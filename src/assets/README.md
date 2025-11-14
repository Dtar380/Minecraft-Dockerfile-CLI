 __  __ _____ _   _ ______ _____ _____            ______ _______   _____   ____   _____ _  ________ _____     _____ _      _____
|  \/  |_   _| \ | |  ____/ ____|  __ \     /\   |  ____|__   __| |  __ \ / __ \ / ____| |/ /  ____|  __ \   / ____| |    |_   _|
| \  / | | | |  \| | |__ | |    | |__) |   /  \  | |__     | |    | |  | | |  | | |    | ' /| |__  | |__) | | |    | |      | |
| |\/| | | | | . ` |  __|| |    |  _  /   / /\ \ |  __|    | |    | |  | | |  | | |    |  < |  __| |  _  /  | |    | |      | |
| |  | |_| |_| |\  | |___| |____| | \ \  / ____ \| |       | |    | |__| | |__| | |____| . \| |____| | \ \  | |____| |____ _| |_
|_|  |_|_____|_| \_|______\_____|_|  \_\/_/    \_\_|       |_|    |_____/ \____/ \_____|_|\_\______|_|  \_\  \_____|______|_____|

MinecraftDockerCLI User Manual.

Your tree file will look something like this:
+---docker-compose.yml
+---README.md
+---data.json
\---servers
    \---server1
        +---.dockerignore
        +---.env
        +---Dockerfile
        +---run.sh
        \---MINECRAFT FILES

Now lets explain what each file does:
- docker-compose.yml is the file in charge of giving docker the information about what each service (container) must look like.
- data.json is the file in charge of storing all the data which is used to later render the docker-compose.yml and .env files.
- servers/ is the folder containing each minecraft server, the user should create this directory and fill them with the required data.
- The server folders should be named accordingly to the service names on the docker-compose.yml
- .dockerignore is the file which tells docker what files should it ignore on build
- .env is the file containing all the environment variables our container will use.
- Dockerfile is the file that docker will use to build the containers
- run.sh is the script the docker containers will use to run the minecraft server.

Minecraft related stuff:
If you are creating a network, we recommend you use velocity as the proxy. Said this, you'll need to take into consideration the next things:
- The proxy connections should look like: {server_name} = {service_name}:port
