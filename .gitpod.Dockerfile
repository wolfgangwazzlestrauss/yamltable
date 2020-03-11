FROM gitpod/workspace-full


# Install additional tools.
RUN RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -yq \
    curl \
    lldb

# Install multiple Python versions.
RUN pyenv install 3.7.5 \
    && pyenv install 3.8.1 \
    && pyenv global 3.8.1

# Install Python packages.
RUN python -m pip install poetry

# Install virtual environment.
RUN poetry install -v
