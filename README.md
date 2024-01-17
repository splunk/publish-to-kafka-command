# alert-action-kafka-publisher
https://splunk.atlassian.net/browse/FDSE-2006 - Publish Splunk events to Kafka via custom streaming command

## Custom Search Command

This custom streaming search command is used to publish Splunk events to Kafka.

### Frontend (Configuration UI)
Uses UCC library (https://splunk.github.io/addonfactory-ucc-generator/)

### Backend (Search command)
- splunklib: https://splunk-python-sdk.readthedocs.io/en/latest/index.html
- solnlib: https://splunk.github.io/addonfactory-solutions-library-python/conf_manager/

### Building and local setup
From within directory `/publish_to_kafka`:
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install UCC
pip install splunk-add-on-ucc-framework

# Build the Splunk app. Should output to 'output' directory
ucc-gen build

# Create symbolic link to output app folder in Splunk apps directory
# Assumes you have set $SPLUNK_HOME
ln -s "$(pwd)/output/publish_to_kafka" "$SPLUNK_HOME/etc/apps/publish_to_kafka"

# Restart Splunk to see the new app
$SPLUNK_HOME/bin/splunk restart
```
Reference: https://splunk.github.io/addonfactory-ucc-generator/quickstart/
### Using the search command
#### Configuration
Open the app, then click on Configuration tab.
Click on Environment tab.
Add a new environment by clicking on "Add" button.
Fill in your environment details.

#### Command example usage
The command sends all preceding Splunk search results as JSON to Kafka.

Assuming you have configured an environment called "dev".
```
|makeresults count=1
| eval hello="world"
| kafkapublish topic_name=test env_name=dev
```
Alternatively, if you don't want to configure an environment, you can specify the environment details in the command itself.
```
|makeresults count=1
| eval hello="world"
| kafkapublish topic_name=test bootstrap_servers="localhost:9092" security_protocol=SASL_PLAINTEXT sasl_plain_username=user sasl_plain_password=pass
```
### Code
Noteworthy files include:
- `publish_to_kafka/package/bin/publish_to_kafka.py`: The search command
- `publish_to_kafka/package/default/command.conf`: The search command configuration
- `publish_to_kafka/package/lib/requirements.txt`: Python dependencies
- `publish_to_kafka/globalConfig.json`: JSON file containing global configuration for the app (UCC)
- `publish_to_kafka/package/appserver/static/js/build/custom/config_env_hook.js`: JS File for custom logic in Config UI

### App Packaging
See https://splunk.github.io/addonfactory-ucc-generator/quickstart/#ucc-gen-package

## Confluent Docker
For testing purposes, included Confluent (including cp-kafka) as docker-compose file.

Derived from https://github.com/confluentinc/cp-all-in-one/blob/7.5.2-post/cp-all-in-one-kraft/docker-compose.yml

Also see: https://docs.confluent.io/platform/current/platform-quickstart.html

### Run
From within directory `/confluent`:

`docker compose up --build`

## Further Reading
Streaming command can run on both SH and indexers:
- https://docs.splunk.com/Documentation/Splunk/9.1.2/Search/Typesofcommands#Distributable_streaming
- Splunklib doc: https://github.com/splunk/splunk-sdk-python/blob/master/splunklib/searchcommands/streaming_command.py#L33-L35
- Performance tuning: https://developer.confluent.io/tutorials/optimize-producer-throughput/confluent.html
  - Compression would help
