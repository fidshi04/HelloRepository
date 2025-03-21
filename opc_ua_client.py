
"""
Einfacher OPC UA-Client

Notwendige Bibliothek installieren:

    apt-get install python3-lxml
    pip3 install opcua 

Für den Zugriff auf Variablen wird die OPC UA Notation genutzt:

    ns=<namespaceIndex>;<identifiertype>=<identifier>
    
    <namespace index> -> namespace index
    <identifier type> -> flag that specifies the identifier type:
                         Flag	Identifier Type
                         i	    NUMERIC (UInteger)
                         s	    STRING (String)
                         g	    GUID (Guid)
                         b	    OPAQUE (ByteString)

Quelle: http://documentation.unified-automation.com/uasdkhp/1.0.0/html/_l2_ua_node_ids.html

"""

from time import sleep
from opcua import Client
from cryptography import x509
from cryptography.hazmat.backends import default_backend


client = Client("opc.tcp://192.168.24.102:4840")
client.set_security_string("Basic256Sha256,SignAndEncrypt,certificate.der,privatekey.pem")
client.application_uri = "urn:unifiedautomation:python-opcua:client"
# setze Benutzername und Passwort
client.set_user('opc')
client.set_password('opc')

try:
    client.connect()

    # greife auf Elemente im Baum zu
    root = client.get_root_node()
    objects = client.get_objects_node()
    app = objects.get_child(["2:DeviceSet", "4:CODESYS Control for Raspberry Pi 64 SL", "4:Resources", "4:Application"])

    """
    # erzeuge Objekte für Knoten aus dem Baum über OPC UA Notation
    eingang1 = client.get_node('ns=4;s=|var|CODESYS Control for Raspberry Pi SL.Application.PLC_PRG.eingang1')
    eingang2 = client.get_node('ns=4;s=|var|CODESYS Control for Raspberry Pi SL.Application.PLC_PRG.eingang2')
    ausgang = client.get_node('ns=4;s=|var|CODESYS Control for Raspberry Pi SL.Application.PLC_PRG.ausgang')
    """

    ausgang_random_value = client.get_node('ns=4;s=|var|CODESYS Control for Raspberry Pi 64 SL.Application.GVL.value')
    # OPC-Variablen besitzen vier Attribute: Datentyp, Wert, Status, Zeitstempel
    data = ausgang_random_value.get_data_value()
    print('************ Variable: Ausgang ************')
    print('Datentyp:    ', data.Value.VariantType)
    print('Wert:        ', data.Value.Value)
    print('Status:      ', data.StatusCode)
    print('Zeitstempel: ', data.SourceTimestamp)
    print('*******************************************')
    """
    # Variable ausgang auslesen
    print('Wert der Variable "ausgang": ', ausgang_.get_value())

    # Variablen eingang1 und eingang2 schreiben
    print('Setzen beider Eingänge auf True!')
    eingang1.set_value(True)
    eingang2.set_value(True)
    sleep(1.0)

    # Variable ausgang auslesen
    print('Wert der Variable "ausgang": ', ausgang.get_value())

    # Variablen eingang1 und eingang2 schreiben
    print('Setzen eines Eingangs auf False!')
    eingang2.set_value(False)
    sleep(1.0)

    # Variable ausgang auslesen
    print('Wert der Variable "ausgang": ', ausgang.get_value())
    """

finally:
    client.disconnect()