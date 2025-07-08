import os

def is_render():
    return os.environ.get("RENDER") == "true"

async def start_docker_container(docker):
    if is_render():
        print("Skipping Docker start on Render")
        return
    await docker.start()

async def stop_docker_container(docker):
    if is_render():
        print("Skipping Docker stop on Render")
        return
    await docker.stop()
