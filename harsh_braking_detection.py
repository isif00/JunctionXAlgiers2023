import json
import asyncio
import math
import websockets


async def receive_data():
    uri = "ws://127.0.0.1:4000"

    init_magnitude = 0
    init_latitude = 0
    init_velocity = 0

    harsh_braking_count = 0
    speeding_count = 0
    experience = 0

    while True:
        async with websockets.connect(uri) as websocket:
            data = await websocket.recv()
            try:
                data_dict = json.loads(data)

                for item in data_dict:
                    id_ = item["bat"]["id"]
                    magnitude = item["bat"]["vl"]
                    latitude = item["gps"]["lat"]

                distance = haversine_distance(
                    init_latitude, init_magnitude, latitude, magnitude
                )
                velocity = (distance * 1000) / (10)

                if (velocity - init_velocity) < 0:
                    print("harsh braking")
                    harsh_braking_count += 1

                if velocity > 0.1:
                    print("speeding")
                    speeding_count += 1

                print(f"{velocity} m/s")

                risk_rating = (harsh_braking_count + speeding_count * 2) / 3
                experience += 1

                final_score = experience / risk_rating

                data_to_return = {
                    "id": id_,
                    "speed": velocity,
                    "final_score": final_score,
                    "harsh_braking_count": harsh_braking_count,
                    "speeding_count": speeding_count,
                    "risk_rating": risk_rating,
                    "experience": experience,
                }

                yield data_to_return

            except json.JSONDecodeError as e:
                print("Error parsing JSON:", e)

        await asyncio.sleep(2)

        init_magnitude = magnitude
        init_latitude = latitude
        init_velocity = velocity


def haversine_distance(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371
    distance = R * c
    return distance
