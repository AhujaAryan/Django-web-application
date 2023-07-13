from rest_framework.decorators import api_view, permission_classes//Importing the api_view and permission_classes decorators from the Django REST Framework.
from rest_framework.permissions import AllowAny//Importing the AllowAny permission class from the Django REST Framework.
from rest_framework.response import Response//Importing the Response class from the Django REST Framework, which is used to create HTTP responses.

from .models import Event, Participant//Importing the Event and Participant models from the current application.
from .serializers import EventSerializer, ParticipantSerializer// Importing the EventSerializer and ParticipantSerializer serializers from the current application.


@api_view(['GET'])
@permission_classes([AllowAny])
def get_upcoming_events(request)://Definition of the get_upcoming_events function, which handles the logic for retrieving a list of upcoming events.
    # Retrieve a list of upcoming events
    events = Event.objects.filter(date__gt=datetime.now())
    serializer = EventSerializer(events, many=True)//Serializing the events queryset using the EventSerializer with many=True parameter, as there can be multiple events.
    return Response(serializer.data)//Returning a HTTP response with the serialized event data.


@api_view(['GET'])//Decorator that marks the following function as an API view that only responds to GET requests.
@permission_classes([AllowAny])//Decorator that specifies the permissions required to access the API view. I to access the view.to any user
def filter_events(request):
    # Filter events based on categories, tags, date, or location
    # Implement your filtering logic here
    filtered_events = ...

    serializer = EventSerializer(filtered_events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def event_details(request, event_id):
    # Retrieve detailed information about an event
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response(status=404)

    serializer = EventSerializer(event)
    return Response(serializer.data)


@api_view(['POST'])
def register_event(request, event_id):
    # Register the authenticated user for an event
    user = request.user
    if not user.is_authenticated:
        return Response({"error": "Authentication required"}, status=401)

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response(status=404)

    # Validate and process registration data
    serializer = ParticipantSerializer(data=request.data)
    if serializer.is_valid():
        participant = serializer.save(user=user, event=event)
        return Response({"participant_id": participant.id}, status=201)

    return Response(serializer.errors, status=400)


@api_view(['POST'])
def rsvp_event(request, event_id):
    # RSVP the authenticated user for an event
    user = request.user
    if not user.is_authenticated:
        return Response({"error": "Authentication required"}, status=401)

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response(status=404)

    # Process RSVP
    participant, created = Participant.objects.get_or_create(user=user, event=event)
    participant.rsvp = True
    participant.save()

    return Response({"participant_id": participant.id})


@api_view(['GET'])
def registration_history(request):
    # Retrieve the registration history of the authenticated user
    user = request.user
    if not user.is_authenticated:
        return Response({"error": "Authentication required"}, status=401)

    registrations = Participant.objects.filter(user=user)
    serializer = ParticipantSerializer(registrations, many=True)
    return Response(serializer.data)
