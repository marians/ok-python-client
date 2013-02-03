# encoding: utf-8

from distutils.core import setup

setup(name='okclient',
    version='0.3',
    author='Marian Steinbach',
    author_email='marian@sendung.de',
    url='https://github.com/marians/ok-python-client',
    packages=['okclient'],
    license="Public Domain",
    description='Client for the Offenes Köln API',
    long_description="""Offenes Köln is a platform that allows for flexible access
to the content of the City of Cologne/Germany's city council information system.

Find more information about the platform at http://offeneskoeln.de/.

More detailed information on the REST API is available at http://offeneskoeln.de/api/.

**Install**

    pip install okclient

**Quick start**

    import okclient
    oc = okclient.Client()

    # Search for documents containing "Haushalt"
    result = oc.documents(query="haushalt")
    for doc in result:
        print doc.date, doc.title

    # Retrieve the document with identifier "3323/2008"
    # including attachments and thumbnails
    result = oc.documents("3323/2008", attachments=True,
                          thumbnails=True)
    print result[0].date, result[0].title
    print result[0].attachments[0].url
    print result[0].attachments[0].content

    # Find streets surrounding a geo position
    # (reverse geocoding)
    streets = oc.streets(lat=50.959, lon=6.946)
    for (name, distance) in streets:
        print "%s is %d meters away" % (name, distance)

    # Find position of street "Mittelstraße"
    # (also called geocoding)
    mittelstr = oc.locations("Mittelstraße")
    # return quasi-centroid of that street
    print mittelstr.averages[0]
    # print out all nodes of that streets
    for node in mittelstr.nodes:
        print node

**Feedback**

Feel free to give feedback via the Issue tracking at https://github.com/marians/ok-python-client.

**Stay tuned**

Stay informed about changes in this client and the API by following our
commits on Github (see URL above), reading our Blog and/or following
the twitter account.

http://blog.offeneskoeln.de/
https://twitter.com/OffenesKoeln
""")
