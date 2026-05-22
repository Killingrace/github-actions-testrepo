import os
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from uvicorn import run

myEnvVar = os.environ.get("myEnvVar", "Development")
counter_file = "data/counter.txt"


async def write_couter(counter: int) -> None:
    try:
        with open(counter_file, "w") as file:
            file.write(str(counter))
    except FileNotFoundError:
        os.mkdir("./data")


async def read_counter() -> int:
    try:
        with open(counter_file, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def hello():
    counter = await read_counter()
    counter += 1
    await write_couter(counter)
    return f"""
        <h2>Hello From Docker!</h2>
        <p>{myEnvVar=}</p>
        <p>{counter=}</p>
        """


@app.get("/logo")
async def logo():
    return FileResponse(path="image.png")


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8080)
