FROM gitpod/workspace-full

ENV PATH /workspace/yamltable/.local/bin:${PATH}

# Install multiple Python versions.
RUN pyenv install 3.7.5 \
    && pyenv install 3.8.1 \
    && pyenv global 3.8.1

# Install Python packages.
RUN python -m pip install --upgrade pip
