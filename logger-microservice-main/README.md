# A logging service that records the activity of other microservices.

### Note that we can read logs and add to them, but you cannot modify or delete pre-existing logs.


**Problem Statement**

Please build a service that provides access to an audit log of events that have taken place within a system of microservices. Services forward events to this service to provide a record of what, when, and where happened. Examples include:

- a new customer account was created for a given identity;
- a customer record was correlated with an external identity / record in another system;
- a customer was billed a certain amount;
- a customer account was deactivated.
The types of events are open-ended. We do not know all kinds of events we might need to add in the future. There will likely be new services created that will need to be audited with new types of events.

Your task is to model an audit trail of events received from such services with a schema that captures the invariant data content along with the variant, application-specific content. Design and (quickly and informally is fine, just capture the intent!) document a microservice API that can receive, store and retrieve these events, and implement it as a proof-of-concept (PoC) HTTP server in Python or Go.

The microservice must be developed in Python or Go and any data storage mechanism may be used for the PoC. In case you decide to use an in-memory data storage, make sure it is concurrency-safe. Simple sequential flat files of records are also fine. Also note that this service is write-mostly, read-seldom.

As this is a PoC you are not expected to solve all possible operational and scalability issues. However, please make notes in the code why you decided to take a shortcut or how it can be addressed in the future as a TODO item for the code reviewer. You will also be asked for a plan to address these concerns in your interview.

Please note that the delivery of the solution must be completed before in-person interviews take place. To review the PoC we will need:

An archive of the source code. Please do not share your solution publicly.
A public URL to a running instance of the service that we will test remotely.
Note that the exercise is meant to be proof-of-concept and is expected to be implemented in one or two evenings. Decide which abstractions are essential and which can be added later to meet these time constraints. It is also perfectly acceptable to submit a not fully functional solution. Of course, more functional implementations will have advantage over non functional ones.

 
**Notes**

1. Server

    a. This application uses Flask, but Flask is not suitable for production environment. We will need to use a WSGI server in production.

    b. Use NGINX for load balancing.

2. Database 

    a. I used MongoDB for the write-heavy application and for sharding the database so that the write throughput is increased.

    b. MongoDB is written to every time a microservice sends an event, but we can modify it so that the `event` is stored inside a list that is appended to every time an event is sent. The insert_many() function can be called once in every few seconds for reducing the number of database calls.

3. General optimization

    a. We can use a queue system such as Redis to handle concurrent write requests (and to not overwhelm the server).

    b. We can cache a part of the logs file for faster access. The part saved would depend upon user statistics, but can default to the tail of the audit.

4. Need to prune requirements.txt file.

5. Currently, most of the code is in app.py inside Services. Need to break it down to a Controller and a Services file.
 


 **References**

 1- https://github.com/GoogleCloudPlatform/microservices-demo
 2- Stackoverflow
