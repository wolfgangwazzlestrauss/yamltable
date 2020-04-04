FROM ubuntu:19.10

# Set system language settings.
ENV LANG=en_US.UTF-8 LC_ALL=C.UTF-8

# Set system timezone to void tzdata interactive prompts.
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Avoid warnings by switching to noninteractive.
ENV DEBIAN_FRONTEND=noninteractive

# Install system packages.
#
# Most packages are required for pyenv as specified at
# https://github.com/pyenv/pyenv/wiki/Common-build-problems#prerequisites.
#
# Flags:
#     -m: Ignore missing or corrupted packages.
#     -q: Quiet for logging.
#     -y: Automatically answer yest to all prompts.
RUN apt-get update -m \
    && apt-get install --no-install-recommends -qy \
        apt-utils \
        bash-completion \
        build-essential \
        curl \
        git \
        libbz2-dev \
        libffi-dev \
        liblzma-dev \
        libncurses5-dev \
        libncursesw5-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        lldb \
        llvm \
        locales \
        python-openssl \
        tk-dev \
        vim \
        wget \
        xz-utils \
        zlib1g-dev \
    # Set system locale.
    && locale-gen en_US.UTF-8 \
    # Clean up package installations.
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /tmp/* \
    && rm -rf /var/lib/apt/lists/*

# Create non-priviledged user.
#
# Flags:
#     -l: Do not add user to lastlog database.
#     -m: Create user home directory if it does not exist.
#     -s /bin/bash: Set user login shell to Bash.
#     -u 1000: Give new user ID value 1000.
RUN useradd -lm -s /bin/bash -u 1000 yamltable

# Switch to non-priviledged user and change directory.
USER yamltable
WORKDIR /home/yamltable

# Add pyenv executables and shims to PATH environment variable.
ENV HOME /home/yamltable
ENV PATH $HOME/.pyenv/bin:$HOME/.pyenv/shims:$PATH
# Add Python scripts directory to PATH environment variable.
ENV PATH /home/yamltable/.local/bin:$PATH

# Install Pyenv and multiple Python interpreter versions with pyenv.
#
# Flags:
#     -L: Follow redirect if requested from endpoint.
#     -S: Show error message if curl request fails.
#     -s: Silent mode, i.e. do not show progress bar.
RUN curl -LSs https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash \
    && { echo; \
        echo 'eval "$(pyenv init -)"'; \
        echo 'eval "$(pyenv virtualenv-init -)"'; } >> .bashrc \
    && pyenv install 3.6.10 \
    && pyenv install 3.7.7 \
    && pyenv install 3.8.2 \
    && pyenv global 3.6.10 \
    && python -m pip install --upgrade pip \
    && python -m pip install --user poetry \
    && rm -rf /tmp/*

# Copy repository files and change their owner.
COPY --chown=yamltable:yamltable . .

# Export Python dependencies from pyproject.toml file.
#
# Flags:
#     --dev: Include development dependencies.
#     -f: Output file format.
#     -o: Output file destination.
#     --without-hashes: Do not include packages hashes.
RUN poetry export --dev --without-hashes -f requirements.txt -o requirements.txt

# Install yamltable and dependencies.
#
# Flags:
#     -e: Install project in development mode.
#     -m: Invoke as module to ensure execution with correct Python version.
#     --progress-bar off: Do not show progress bar.
#     -r: Install from requirements files.
#     --user: Install to Python user directory.
RUN python -m pip install --user --progress-bar off -r requirements.txt .

CMD ["/bin/bash"]
