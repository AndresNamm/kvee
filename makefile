BUCKET=aws-kronotech-deployments
ifdef SOURCE
	TEMPLATE_NAME="templates/template-${SOURCE}.yaml"
	PACKAGED_NAME="templates/packaged-${SOURCE}.yaml"
endif

ifdef SANDBOX
	TEMPLATE_NAME="sandbox_templates/template-${SOURCE}.yaml"
	PACKAGED_NAME="sandbox_templates/packaged-${SOURCE}.yaml"
endif


PARAM=
ifdef HOSTING
	PARAM= HostingParameter=$(HOSTING)
endif

ENV="dev"
ifdef ENVIRONMENT
	ENV=$(ENVIRONMENT)
endif
AWS_REGION=eu-west-1

setup:
	sam build -t ${TEMPLATE_NAME} -u
package: setup
	sam package\
        --s3-bucket $(BUCKET) \
        --region eu-west-1 \
        --output-template-file $(PACKAGED_NAME)

deploy: package	
	sam deploy --region $(AWS_REGION) \
		--template-file $(PACKAGED_NAME) \
		--stack-name $(ENV)-${SOURCE} \
		--parameter-overrides EnvironmentParameter=$(ENV) $(PARAM) \
		--capabilities CAPABILITY_IAM

package-ssm: 
	sam package --template-file $(TEMPLATE_NAME) \
        --s3-bucket $(BUCKET) \
        --region eu-west-1 \
        --output-template-file $(PACKAGED_NAME)

deploy-ssm: package-ssm
	sam deploy --region $(AWS_REGION) \
		--template-file $(PACKAGED_NAME) \
		--stack-name $(ENV)-${SOURCE} \
		--parameter-overrides EnvironmentParameter=$(ENV) $(PARAM) \
		--capabilities CAPABILITY_IAM

