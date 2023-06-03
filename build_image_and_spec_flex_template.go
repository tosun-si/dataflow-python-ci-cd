package main

import (
	"context"
	"fmt"
	"os"

	"dagger.io/dagger"
)

func main() {
	projectId := os.Getenv("PROJECT_ID")
	location := os.Getenv("LOCATION")
	repoName := os.Getenv("REPO_NAME")
	imageName := os.Getenv("IMAGE_NAME")
	imageTag := os.Getenv("IMAGE_TAG")
	metadataTemplateFilePath := os.Getenv("METADATA_TEMPLATE_FILE_PATH")
	sdkLanguage := os.Getenv("SDK_LANGUAGE")
	metadataFile := os.Getenv("METADATA_FILE")
	saEmail := os.Getenv("SA_EMAIL")

	ctx := context.Background()
	client, err := dagger.Connect(ctx, dagger.WithLogOutput(os.Stdout))

	if err != nil {
		panic(err)
	}
	defer client.Close()

	hostSourceDir := client.Host().Directory(".", dagger.HostDirectoryOpts{})

	activateServiceAccount := []string{
		"gcloud",
		"auth",
		"activate-service-account",
		saEmail,
		"--key-file=./secrets/sa-dataflow.json",
		fmt.Sprintf("--project=%s", projectId),
	}

	source := client.Container().
		From("google/cloud-sdk:420.0.0-slim").
		WithMountedDirectory("/src", hostSourceDir).
		WithWorkdir("/src").
		Directory(".")

	buildFlexTemplateImage := client.Container().
		From("gcr.io/kaniko-project/executor:v1.9.0-debug").
		WithEntrypoint([]string{}).
		WithDirectory(".", source).
		WithEnvVariable("CI_SERVICE_NAME", "dagger").
		WithEnvVariable("PROJECT_ID", projectId).
		WithEnvVariable("LOCATION", location).
		WithEnvVariable("REPO_NAME", repoName).
		WithEnvVariable("IMAGE_NAME", imageName).
		WithEnvVariable("IMAGE_TAG", imageTag).
		WithEnvVariable("GOOGLE_APPLICATION_CREDENTIALS", "./secrets/sa-dataflow.json").
		WithExec([]string{
			"sh",
			"-c",
			"/kaniko/executor --use-new-run --single-snapshot --context=dir://./ --dockerfile Dockerfile --destination $LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME/$CI_SERVICE_NAME:$IMAGE_TAG",
		}).
		Directory(".")

	createFlexTemplateSpecFileGcs := client.Container().
		From("google/cloud-sdk:420.0.0-slim").
		WithDirectory(".", buildFlexTemplateImage).
		WithEnvVariable("CI_SERVICE_NAME", "dagger").
		WithEnvVariable("PROJECT_ID", projectId).
		WithEnvVariable("LOCATION", location).
		WithEnvVariable("REPO_NAME", repoName).
		WithEnvVariable("IMAGE_NAME", imageName).
		WithEnvVariable("IMAGE_TAG", imageTag).
		WithEnvVariable("METADATA_TEMPLATE_FILE_PATH", metadataTemplateFilePath).
		WithEnvVariable("SDK_LANGUAGE", sdkLanguage).
		WithEnvVariable("METADATA_FILE", metadataFile).
		WithEnvVariable("GOOGLE_APPLICATION_CREDENTIALS", "./secrets/sa-dataflow.json").
		WithExec(activateServiceAccount).
		WithExec([]string{
			"sh",
			"-c",
			"./scripts/create_flex_template_spec_file_gcs.sh",
		})

	out, err := createFlexTemplateSpecFileGcs.Stdout(ctx)

	if err != nil {
		panic(err)
	}

	fmt.Printf("Published image to: %s\n", out)
}
