# syntax = docker/dockerfile:1.2
# ^ This enables the new BuildKit stable syntax which can be
# run with the DOCKER_BUILDKIT=1 environment variable in your
# docker build command (see build.sh)
FROM debian:buster-slim

# Update, upgrade, and cleanup debian packages
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get upgrade --yes && \
    apt-get install --yes stress-ng && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["stress-ng", "--cpu", "1", "--timeout", "600"]
