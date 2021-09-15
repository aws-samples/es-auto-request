# Automatically request Enterprise Support for newly created accounts

This sample repository helps you to deploy a simple solution to watch for newly created accounts in your organization and submit a support case requesting the new account to have Enterprise Support enabled.

This CloudFormation template will create in your account:
1. An IAM role with permissions to execute your Lambda function, and interact with AWS Support API.
1. AWS Lambda function, that will submit the support case requesting Enterprise Support to be enabled in the newly created account
1. EventBridge Rule, which will be matching the event for `CreateAccountResult` and passing this event to AWS Lambda
1. AWS Lambda Permission, which allows the event from EventBridge rule to trigger the AWS Lambda.

# Workflow
![Alt text](images/diagram.png?raw=true "Enabling Enterprise Support")

1. When you create a new account in your organization, a new event `CreateAccountResult` will be generated in your CloudTrail.
2. The EventBridge rule will match this event if the creation state is `SUCCEEDED` and trigger the AWS Lambda function for processing, passing the whole Event body to the function.
3. The Lambda function will parse the Event body and look for the `Account ID` of the newly created account.
4. Having the `Account ID`, the function will connect to the AWS Support API and submit the support case, requesting Enterprise Support to be enabled on the newly created account. The support case will be created with a `Production System Impaired` severity.

# Setup

To facilitate the implementation of this solution, you can simply deploy the CloudFormation template from this repository. You can also find the `EventSample.json` and `rule.json` used for this implementation on the `samples` directory and use this information to build the same manually if you prefer.

-  **Download or clone the repository**

To start the deployment, clone this repository to the desired location, or download it as a ZIP file. On this example, I will be downloading it as a ZIP file. 

![Alt text](images/download-zip.png?raw=true "Downloading the repo")

- **Extract files**

Extract the files from the ZIP

- **Open your AWS Managed Console**

Using your preferred browser, open the [AWS Managed Console](https://console.aws.amazon.com/console/home?region=us-east-1 "AWS Managed Console").

- **Navigate to the CloudFormation console**

![Alt text](images/setup/1.png?raw=true "Managed Console CloudFormation")

- **Create a new Stack**

On the top right corner of the page, click on `Create stack` -> `With new resources (standard)`

![Alt text](images/setup/2.png?raw=true "Create stack")

In the `Prerequisite - Prepare template` session, make sure the `Template is ready` option is selected.

For the `Specify template`, select `Upload a template file` and choose the `EnableES.yaml` file you downloaded from this repository.

![Alt text](images/setup/3.png?raw=true "Downloading the repo")

Click in `Next`.

On the `Specify stack details` section, provide a name to your stack. This name will be added to the name of resources created on the stack. I will choose `EnableES` as stack name.

Click in `Next`.

![Alt text](images/setup/4.png?raw=true "Stack options")

On the `Configure stack options` section, you can provide Tags if you wish. Leave all the remaining fields as default. 

On the bottom of the page, click `Next`.


![Alt text](images/setup/5.png?raw=true "Review page")

On the `Review STACK_NAME` page, scroll all the way down, make sure the check box `I acknowledge that AWS CloudFormation might create IAM resources` is checked, and click in `Create stack`.

![Alt text](images/setup/6.png?raw=true "Create stack")

The setup process might take a few minutes to complete.
Click on the `Refresh` icon until you see `CREATE_COMPLETE` for the stack.

![Alt text](images/setup/7.png?raw=true "Create Complete")

# Validation

To validate the setup was completed successfully, check the `Resources` tab of your newly created Stack. 

![Alt text](images/setup/8.png?raw=true "Stack resources")

Click on the `EnableESFunction` Physical ID to open the AWS Lambda Function. 

![Alt text](images/setup/9.png?raw=true "Stack resources, open function")

It will open the AWS Lambda Function in a new tab of your browser. 

In the Lambda Function page, you should be able to see the `EventBridge (CloudWatch)` as a trigger for the code.
Seeing the `EventBridge (CloudWatch)` as the trigger for the code indicates the Lambda permissions are set correctly and EventBridge is able to invoke the function.

![Alt text](images/setup/10.png?raw=true "Lambda design")

Click in the `EventBridge (CloudWatch)` to see available triggers for this function.

Only `EventBridge (CloudWatch Events): NewAccountRule` should be listed as a trigger.

![Alt text](images/setup/11.png?raw=true "Lambda trigger list")

You can click on `Details` to verify the Event pattern to match this rule.

![Alt text](images/setup/12.png?raw=true "Lambda trigger details")

On the left panel for your Lambda function, click on `Permissions` to validate the IAM Role associated with the function.

![Alt text](images/setup/13.png?raw=true "Left panel")

You will see there is a role associated with the function. This role name must start with `EnableES-EnableESRole-` and is the role that authorizes the function to be executed and to communicate with AWS Support API, submiting the support case to request enabling Enterprise Support on the newly created account.

![Alt text](images/setup/14.png?raw=true "List of roles")

If you click on the role name to see the details about the role, expand the `AutoES` policy to see the operations the role is allowed to perform.

![Alt text](images/setup/15.png?raw=true "Role policy")

If you confirm all the the steps of this document were executed as expected, the next you create a new account in your organization, it will automatically submit a support case requesting Enterprise Support to be enabled in the newly created account with a Production System Impaired severity.

![Alt text](images/setup/16.png?raw=true "Support case example")

# Cleanup
Once you confirmed the automation to request enabling Enterprise Support on the newly created account works as exected, if you decide to delete all the associated resources:
* Navigate again to the CloudFormation console, 
* List your stacks
* Select the `EnableES` stack
* Click on `Delete`
* Click on `Delete stack` to confirm your action
* Wait until the deletion is completed 

