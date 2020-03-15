# "Global" makefile

COMPONENTS  = local_beauty local_aggry local_forwarder local_storage local_mysql
DCL         = mclaren.yml
STACK       = mclaren


.PHONY: build
build:
	for service in $(COMPONENTS); do make -C "$$service" build || break; done

# deploy only if nothing is running
.PHONY: deploy
deploy:
	@ docker stack ps -q $(STACK) > /dev/null 2>&1 && { echo "Make sure you 'undeploy' first"; } || { docker stack deploy $(STACK) -c $(DCL); }

.PHONY: undeploy
undeploy:
	@docker stack rm $(STACK) 2>&1

.PHONY: status
status:
	@docker stack ps $(STACK) --no-trunc

.PHONY: all
all: build deploy

.PHONY: logs
logs:
	@docker service logs $(STACK)_aggry

.PHONY: logs_forwarder
logs_forwarder:
	@docker service logs $(STACK)_mqtt_to_websocket

.PHONY: logs_storage
logs_storage:
	@docker service logs $(STACK)_storage

.PHONY: logs_webapp
logs_webapp:
	@docker service logs $(STACK)_webapp

.PHONY: logs_mysql
logs_mysql:
	@docker service logs $(STACK)_mysql

.PHONE: clear_data
clear_data:
	@mv local_mysql/data/README.md local_mysql/_README.md
	@rm -rf local_mysql/data/[0-9]*  local_mysql/data/[a-z]*
	@mkdir -p local_mysql/data
	@mv local_mysql/_README.md local_mysql/data/README.md


# EOF #
