# Rust-Executor-Server

A simple implementation of rust executor server using fastapi.

- Platform: Linux
- Language: Python

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py --port 8000 --host 0.0.0.0
```

## API
```python
curl -X 'POST' \
  'http://127.0.0.1:8000/run_rust_code' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "rust_code": "fn main() { println!(\"Hello, world!\"); }"
}'

```