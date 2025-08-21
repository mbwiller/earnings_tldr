.PHONY: help dev test run eval demo clean docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make dev    - Install dependencies"
	@echo "  make test   - Run tests"
	@echo "  make run    - Run application"
	@echo "  make demo   - Run offline demo"
	@echo "  make clean  - Clean generated files"

dev:
	cd server && pip install -r requirements.txt
	cd web && npm install
	cp .env.example .env

test:
	cd server && python -m pytest tests/ -v
	cd web && npm test

run:
	@trap 'kill %1' INT; \
	(cd server && uvicorn main:app --reload) & \
	(cd web && npm run dev) & \
	wait

demo:
	OFFLINE_MODE=true $(MAKE) run

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf web/.next web/node_modules
	rm -rf data/processed/* data/cache/*

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down
