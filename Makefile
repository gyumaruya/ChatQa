STAGE=prod

.PHONY: build
build:
	DOCKER_BUILDKIT=1 \
	docker build \
	-t chatqa:$(STAGE) \
	-f ./docker/Dockerfile ./docker


.PHONY: debug
debug:
	docker run \
		--rm -it \
		--net bridge \
		 -p 8501:8501 \
		-v $(PWD):/app \
		--name chatqa \
		-w /app/src chatqa:$(STAGE) bash

.PHONY: run
run:
	docker run \
		--rm -d \
		--net bridge \
		-p 8501:8501 \
		-v $(PWD):/app \
		--name chatqa \
		-w /app/src \
		chatqa:$(STAGE) streamlit run main.py