FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

ARG WORKDIR=/template
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

COPY . ${WORKDIR}/

RUN ls -R ${WORKDIR}

ENV PYTHONPATH ${WORKDIR}

ENV REQUIREMENTS_FILE="${WORKDIR}/team_league/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE="${WORKDIR}/setup.py"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/team_league/application/team_league_app.py"

# We could get rid of installing libffi-dev and git, or we could leave them.
#RUN apt-get update \
#    && apt-get install -y libffi-dev git \
#    && rm -rf /var/lib/apt/lists/* \
#    # Upgrade pip and install the requirements.
#    && pip install --no-cache-dir --upgrade pip \
#    && pip install --no-cache-dir -r $REQUIREMENTS_FILE \
#    # Download the requirements to speed up launching the Dataflow job.
#    && pip download --no-cache-dir --dest /tmp/dataflow-requirements-cache -r $REQUIREMENTS_FILE \

RUN apt-get update \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir 'apache-beam[gcp]==2.47.0' \
    && pip install --no-cache-dir -r $REQUIREMENTS_FILE

#RUN python ${WORKDIR}/setup.py install

# Since we already downloaded all the dependencies, there's no need to rebuild everything.
ENV PIP_NO_DEPS=True

ENTRYPOINT ["/opt/google/dataflow/python_template_launcher"]
