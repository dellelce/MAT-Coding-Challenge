# MyTutor Test Makefile

VENV := mclaren-env
TERRAFORM := $(PWD)/bin/terraform
TERRAVERS := 0.12.19
TERRAURL := https://releases.hashicorp.com/terraform/$(TERRAVERS)/terraform_$(TERRAVERS)_linux_amd64.zip
KEYS := terraform/ec2.key
SSHOPTS := -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null
CERTS = $$( python -c 'import certifi; print(certifi.where());' )

ip = $$( cd terraform && $(TERRAFORM)  output -json instance_ips | awk -F\" ' { print $$2 } '  )

help:
	@cat docs/help.txt

pyvenv:
	@python3 -m venv $(VENV) && .  $(VENV)/bin/activate && pip install -r requirements.txt -U pip setuptools

# "shortcut" to next target
terrabin: bin/terraform

# download and "install" terraform
bin/terraform:
	@wget -q -O bin/terraform.zip $(TERRAURL) && cd bin && unzip -q terraform.zip && chmod +x terraform && rm terraform.zip

terraversion:
	@$(TERRAFORM) version

init:
	@cd terraform && $(TERRAFORM) init

plan:
	@cd terraform && $(TERRAFORM) plan

apply:
	@cd terraform && $(TERRAFORM) apply -input=false

apply_force:
	@cd terraform && $(TERRAFORM) apply -auto-approve -input=false

show:
	@cd terraform && $(TERRAFORM) show

destroy:
	@cd terraform && $(TERRAFORM) destroy

$(KEYS):
	@ssh-keygen -t rsa -b 2048 -f $(KEYS) -N ""

keys: $(KEYS)

output:
	@cd terraform && $(TERRAFORM) output instance_ips

ip:
	@echo $(ip)

ssh:
	@ssh -i $(KEYS) $(SSHOPTS) $(SYSUSER)@$(ip)

test_client:
	@. $(VENV)/bin/activate && aws sts get-caller-identity

# include MacLaren specific targets
include mclaren.mk
