######################################################################################################################################################

# @project        Space Elevator ▸ LEDs Strip
# @file           Makefile
# @author         <info@spacelevator.org>
# @license        Space Elevator 2022

######################################################################################################################################################

build:
	docker build --tag leds-strip .

run: build
	docker run \
		-v $(CURDIR)/config.json:/app/config.json \
		-v /dev:/dev \
		--privileged \
		--rm \
		leds-strip

up:
	docker-compose up -d

down:
	docker-compose down

######################################################################################################################################################
