# python3 pubsub.py --topic topic_1 --ca_file ~/certs/Amazon-root-CA-1.pem --cert ~/certs/certificate.pem.crt --key ~/certs/private.pem.key --endpoint a33s1cpy5ai1k0-ats.iot.us-east-1.amazonaws.com

from awscrt import mqtt
from awsiot import mqtt_connection_builder
import json
import sys

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


def on_resubscribe_complete(resubscribe_future):
        resubscribe_results = resubscribe_future.result()
        print("Resubscribe results: {}".format(resubscribe_results))

        for topic, qos in resubscribe_results['topics']:
            if qos is None:
                sys.exit("Server rejected resubscribe to topic: {}".format(topic))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)

class MQTT:
    TOPIC = "device/23/data"
    CA_FILE = "/home/pi//certs/Amazon-root-CA-1.pem"
    CERT = "/home/pi//certs/certificate.pem.crt"
    KEY  = "/home/pi//certs/private.pem.key"
    ENDPOINT = "a33s1cpy5ai1k0-ats.iot.us-east-1.amazonaws.com"

    def build_mqtt_connection(self):
        # proxy_options = self.get_proxy_options_for_mqtt_connection()
        mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=self.ENDPOINT,
            # port=8080,
            cert_filepath=self.CERT,
            pri_key_filepath=self.KEY,
            ca_filepath=self.CA_FILE,
            on_connection_interrupted=on_connection_interrupted,
            on_connection_resumed=on_connection_resumed,
            client_id="autoDrip",
            clean_session=False,
            keep_alive_secs=30,
            # http_proxy_options=proxy_options
            )
        return mqtt_connection

    def publish(self, message):
        mqtt_connection = self.build_mqtt_connection()
        connect_future = mqtt_connection.connect()

        # Future.result() waits until a result is available
        connect_future.result()
        print("Connected!")

        message_json = json.dumps(message)
        mqtt_connection.publish(
            topic=self.TOPIC,
            payload=message_json,
            qos=mqtt.QoS.AT_LEAST_ONCE)

        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()
