ok-python-client
================

Python Client für die Offenes Köln API

## Installation

    pip install okclient

## Quickstart

    import okclient
    
    oc = okclient.Client()

    # Suche nach Dokumente mit dem Begriff "haushalt"
    result = oc.documents(query="haushalt")
    for doc in result:
        print doc.date, doc.title
    
    # Dokument mit der Kennung "3323/2008" abholen,
    # mit Attachments und Thumbnails
    result = oc.documents("3323/2008", attachments=True,
                          thumbnails=True)
    print result[0].date, result[0].title
    print result[0].attachments[0].url
    print result[0].attachments[0].content

    # Position der "Mittelstraße" abrufen
    mittelstr = oc.locations("Mittelstraße")
    # Mittelpunkt der Mitteltraße ausgeben
    print mittelstraße.averages[0]
    # Knoten der Mittelstraße ausgeben
    for node in mittelstraße.nodes:
        print node


## Status

Bisher werden die folgenden API-Methoden unterstützt:

 * documents (/api/documents) zum Abruf von Dokumenten
 * locations (/api/locations) zum Abruf von Ortsinformationen zu Straßen und Plätzen

Der Zugriff auf die anderen API-Methoden (siehe http://offeneskoeln.de/api/) ist noch nicht implementiert.

## Feedback

ist immer herzlich willkommen! Bitte benutzt die Seite "Issues" in der Navigation. Oder schickt Pull Requests.

## Lizenz

Public Domain

## Weitere Info

* Offenes Köln: http://offeneskoeln.de/
* Blog: http://blog.offeneskoeln.de/
* Twitter: https://twitter.com/OffenesKoeln
* Facebook: http://www.facebook.com/offeneskoeln
