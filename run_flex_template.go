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
	jobName := os.Getenv("JOB_NAME")
	metadataTemplateFilePath := os.Getenv("METADATA_TEMPLATE_FILE_PATH")
	tempLocation := os.Getenv("TEMP_LOCATION")
	stagingLocation := os.Getenv("STAGING_LOCATION")
	saEmail := os.Getenv("SA_EMAIL")
	inputFile := os.Getenv("INPUT_FILE")
	teamLeagueDataset := os.Getenv("TEAM_LEAGUE_DATASET")
	teamLeagueTable := os.Getenv("TEAM_STATS_TABLE")

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

	runFlexTemplate := client.Container().
		From("google/cloud-sdk:420.0.0-slim").
		WithDirectory(".", source).
		WithEnvVariable("PROJECT_ID", projectId).
		WithEnvVariable("LOCATION", location).
		WithEnvVariable("JOB_NAME", jobName).
		WithEnvVariable("METADATA_TEMPLATE_FILE_PATH", metadataTemplateFilePath).
		WithEnvVariable("TEMP_LOCATION", tempLocation).
		WithEnvVariable("STAGING_LOCATION", stagingLocation).
		WithEnvVariable("SA_EMAIL", saEmail).
		WithEnvVariable("INPUT_FILE", inputFile).
		WithEnvVariable("TEAM_LEAGUE_DATASET", teamLeagueDataset).
		WithEnvVariable("TEAM_STATS_TABLE", teamLeagueTable).
		WithEnvVariable("GOOGLE_APPLICATION_CREDENTIALS", "./secrets/sa-dataflow.json").
		WithExec(activateServiceAccount).
		WithExec([]string{
			"sh",
			"-c",
			"./scripts/run_dataflow_job.sh",
		})

	out, err := runFlexTemplate.Stdout(ctx)

	if err != nil {
		panic(err)
	}

	fmt.Printf("Published image to: %s\n", out)
}
