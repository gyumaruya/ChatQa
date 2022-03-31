# Copyright © 2022 gyumaruya gyumaru7a@gmail.com

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM python:3.9.11-bullseye as builder
USER root

RUN DEBIAN_FRONTEND="noninteractive" apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
    locales

RUN DEBIAN_FRONTEND="noninteractive" \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

ENV LANG="ja_JP.UTF-8"
ENV LANGUAGE="ja_JP:ja"
ENV LC_ALL="ja_JP.UTF-8"
ENV TZ="JST-9"
ENV TERM="xterm"
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/root/.local/lib/python3.9/site-packages:$PYTHONPATH

RUN pip install --user -U pip
RUN pip install --user -U setuptools wheel
COPY ./requirements.txt /tmp/requirements.txt 
RUN pip install --user -U -r /tmp/requirements.txt 

FROM python:3.9.11-slim-bullseye

ENV LANG="ja_JP.UTF-8"
ENV LANGUAGE="ja_JP:ja"
ENV LC_ALL="ja_JP.UTF-8"
ENV TZ="JST-9"
ENV TERM="xterm"
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/root/.local/lib/python3.9/site-packages:$PYTHONPATH
COPY --from=builder /root/.local /root/.local