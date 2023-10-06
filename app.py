import asyncio
from flask import Flask, jsonify
from harsh_braking_detection import receive_data


app = Flask(__name__)


@app.route("/get_data", methods=["GET"])
def get_data():
    data_list = []

    async def collect_data():
        async for data in receive_data():
            data_list.append(data)
            break

    asyncio.run(collect_data())
    return jsonify(data_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
