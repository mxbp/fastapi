#!/usr/bin/env python3
import os
from typing import List

import asyncpg
import uvicorn
from fastapi import FastAPI, Depends

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/healthz")
async def read_root():
    return {"status": "Ok"}


async def get_db():
    postgres_user = os.getenv("POSTGRES_USER", "postgres")
    postgres_pass = os.getenv("POSTGRES_PASS", "postgres")
    postgres_host = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port = os.getenv("POSTGRES_PORT", "5432")
    postgres_db = os.getenv("POSTGRES_DB", "postgres")

    conn = await asyncpg.connect(f"postgresql://{postgres_user}:{postgres_pass}@{postgres_host}:{postgres_port}/{postgres_db}")
    try:
        yield conn
    finally:
        await conn.close()


@app.get("/db", response_model=List[dict])
async def read_items(db=Depends(get_db)):
    rows = await db.fetch("SELECT id, name FROM items;")
    return [dict(row) for row in rows]


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8080, reload=True, log_level="info")
