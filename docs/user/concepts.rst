Important Concepts
==================

.. _concepts_uids:

UIDs
----
Unique identifiers (UIDs) are a way of identifying a wide variety
of items in a way that guarantees uniqueness across multiple countries, sites,
vendors and equipment. The UID identification scheme used by DICOM is based on
the numeric form of the OSI Object Identification as defined by
`ISO/IEC 8824 <https://www.iso.org/standard/68350.html>`_
(`ITU X.680 <https://www.itu.int/itu-t/recommendations/rec.aspx?rec=x.680>`_).

Each UID is composed of two parts, an ``<org root>`` and a ``<suffix>``:
``UID = <org root>.<suffix>``


The ``<org root>`` uniquely identifies an organisation and is composed of
numeric components as defined by ISO/IEC 8824. The ``<suffix>`` portion of the
UID is also composed of a number of numeric components, however it is generated
by the application and must be unique within the scope of the ``<org root>``.
If you don't have an ``<org root>`` and you don't want to use *pynetdicom's*
(``1.2.826.0.1.3680043.9.3811``) an ``<org root>`` can be obtained for free
from the `Medical Connections <https://www.medicalconnections.co.uk/FreeUID/>`_
website.

The DICOM ``<org root>`` is ``1.2.840.10008`` and is reserved for use for DICOM
defined items and shall not be used for privately defined items. As an example,
the official DICOM UID for *CT Image Storage* is
``1.2.840.10008.5.1.4.1.1.2``, which makes the ``<suffix>`` ``5.1.4.1.1.2``

Each component of a UID (``1``, ``2``, ``840``, ``10008`` are all components)
must not start with ``0`` unless the component itself is ``0`` (e.g.
``1.2.0.4`` is valid but ``1.2.08.4`` is invalid) and the maximum length of a
UID is 64 total characters.

More information on DICOM UIDs is available in :dcm:`Part 5 <part05.html>`
of the DICOM Standard.


DICOM Information Model
-----------------------

.. _concepts_iods:

Information Object Definition (IOD)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
An IOD is an object-orientated abstract data model use to specify information
about a class of real-world objects that share the same properties.
For example, a *Patient*, a *Study*, an imaging *Series* and a piece of imaging
*Equipment* are all real world objects. An IOD, then, is the data model used to
define the relationship between the objects (the *Patient* has
one or more *Studies*, each *Study* contains one or more *Series* and each
*Series* is created by a piece of *Equipment*).

IODs come in two types; composite and normalised IODs. Normalised IODs
generally represent only a single class of real-world objects (such as the
:dcm:`Print Job IOD <part03/sect_B.11.2.html>`). Composite IODs include
information about related real-world objects (such as the
:dcm:`CT Image IOD <part03/sect_A.3.3.html>` which contains objects like
*Patient*, *Study*, *Series*, *Equipment*, etc).

There are many different DICOM IODs and they're all defined in
:dcm:`Part 3 <part03.html>` of the DICOM Standard.

.. _concepts_sop_classes:

SOP Classes
~~~~~~~~~~~
A Service-Object Pair (SOP) Class is defined by the union of an IOD and a
:dcm:`DICOM Message Service Element <part07/PS3.7.html>`
(DIMSE) service group:

* **Composite SOP Classes** are the union of Composite IODs and
  the DIMSE-C service group. An example of a Composite SOP Class is the
  *CT Image Storage SOP Class*, which is the union of the *CT Image IOD* and
  the DIMSE C-STORE service. A *CT Image Storage* instance stores information
  about a single slice of a patient's CT scan. A complete scan (a *Series*) is
  made up of one or more *CT Image Storage SOP Class* instances, all
  with the same *Study Instance UID* and *Series Instance UID* values but
  differing *SOP Instance UID* values (one for each SOP instance within the
  *Series*).
* **Normalised SOP Classes** are the union of Normalised IODs and DIMSE-N
  service group. An example of a Normalised SOP Class is the *Print Job SOP
  Class*, which is the union of the *Print Job IOD* and the DIMSE
  N-EVENT-REPORT and N-GET services. The *Print Job SOP Class* is an
  abstraction of a print job containing one or more films to be printed.

The DIMSE-C and DIMSE-N services are defined in :dcm:`Part 7<part07.html>` of
the DICOM Standard. Every DICOM SOP class has its own UID that can be found in
:dcm:`Part 6<part06/chapter_A.html>`.


.. _concepts_service_classes:

Service Classes
~~~~~~~~~~~~~~~
A DICOM Service Class defines a group of one or more SOP Classes related to a
service that is to be used by communicating application  entities, as well as
the rules that are to govern the provision of the service. Services
include storage of SOP Class instances (*Storage Service Class*), verification
of DICOM connectivity (*Verification Service Class*), querying and retrieval
of managed SOP instances (*Query/Retrieve Service Class*), printing of images
(*Print Management Service Class*) and many others.

The labels *Service Class User* and *Service Class Provider* are derived from
whether or not an AE *uses* or *provides* the services in a Service Class.

Service Classes are defined in :dcm:`Part 4<part04.html>` of the DICOM
Standard.


.. _concepts_ae:

Application Entities
--------------------
A DICOM *Application Entity* (AE) is an application that supports the DICOM
standard in general, and especially IODs, service classes and dataset
encoding/decoding.

In DICOM networking, AEs are identified by their *AE Title*.


.. _concepts_presentation_contexts:

Presentation Contexts
---------------------
Presentation Contexts are used during the negotiation of an association to
provide a method for communicating AEs to agree on a set of supported services.
Each Presentation Context consists of an Abstract Syntax and one or more
Transfer Syntaxes, along with an ID value.

* The association *requestor* may propose multiple presentation contexts per
  association but is limited to a maximum of 128 proposed contexts.
* Each proposed presentation context contains one Abstract Syntax and one or
  more Transfer Syntaxes.
* The *requestor* may propose multiple contexts with the same Abstract Syntax
* The association *acceptor* may accept or reject each presentation context
  individually, but only one Transfer Syntax may be accepted per presentation
  context.
* The *acceptor* selects a suitable Transfer Syntax for each accepted
  presentation context.

A more detailed guide to presentation contexts and how to use them with
*pynetdicom* is available :ref:`here <user_presentation>`.

.. _concepts_abstract_syntax:

Abstract Syntax
~~~~~~~~~~~~~~~
An :dcm:`Abstract Syntax<part08/chapter_B.html>`
is a specification of a set of data elements and their associated semantics.
Each Abstract Syntax is identified by an *Abstract Syntax Name* in the form
of a UID. Abstract syntax names used with DICOM are usually the officially
registered SOP class UIDs (and the abstract syntax is therefore the SOP class
itself), but the standard also allows the use of private
abstract syntaxes. While *pynetdicom* can handle association negotiation
containing private abstract syntaxes the implementation of the associated
services/semantics is up to the end user.

.. _concepts_transfer_syntax:

Transfer Syntax
~~~~~~~~~~~~~~~
A :dcm:`Transfer Syntax<part08/sect_B.2.html>`
defines a set of encoding rules able to unambiguously
represent the data elements defined by one or more Abstract Syntaxes. In
particular, the negotiation of transfer syntaxes allows communicating AEs to
agree on the encoding techniques they are able to support (i.e. byte ordering,
compression, etc.).

The official DICOM transfer syntaxes are defined in
:dcm:`Part 5<part05.html#chapter_8>` of the DICOM Standard. The Standard also
allows the use of privately defined transfer syntaxes. While *pynetdicom* is
able to handle association negotiation containing private transfer syntaxes,
the implementation of the associated encoding requirements is the
responsibility of the end user.


.. _concepts_association:

Association
-----------
When peer AEs want to communicate they must first establish an Association.

* The AE that is initiating the association (the *Requestor*) sends
  an A-ASSOCIATE message to the peer AE (the *Acceptor*) which contains a list
  of proposed presentation contexts and association negotiation items.
* The *acceptor* receives the request and responds with:

  * acceptance, which results is an association being established, or
  * rejection, which results in no association, or
  * abort, which results in no association

An association may be rejected because none of the proposed presentation
contexts are supported, or because the *Requestor* hasn't identified itself
correctly or for a :dcm:`number of other reasons<part08/sect_9.3.4.html>`.

The full service procedure for an association is found in
:dcm:`Part 8<part08/chapter_7.html#sect_7.1.2>` of the DICOM Standard.

.. _concepts_negotiation:

Association Negotiation and Extended Negotiation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Standard association negotiation usually involves the peer AEs agreeing on a
set of abstract syntax/transfer syntax combinations through the mechanism
provided by presentation contexts. In some cases it may be necessary for
communicating AEs to exchange more detailed information about features and
services they may optionally require/support. This is accomplished by sending
additional user information items during the association request:

* Asynchronous Operations Window Negotiation
* SCP/SCU Role Selection Negotiation
* SOP Class Extended Negotiation
* SOP Class Common Extended Negotiation
* User Identity Negotiation

Some of these items are conditionally required,
depending on the requested service class (such as SCP/SCU role selection
negotiation when the Query/Retrieve service class' C-GET operation is
requested). Association negotiation involving these additional items is usually
referred to as *extended negotiation*.

Extended negotiation items are defined in :dcm:`Part 7<part07/chapter_D.html>`
and :dcm:`Part 8<part08/chapter_D.html>` of the DICOM Standard.
