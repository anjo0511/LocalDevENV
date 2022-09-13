

from python_on_whales import DockerClient, docker

containers_on = docker.container.list(all=False, filters={})


print([x.name for x in containers_on])