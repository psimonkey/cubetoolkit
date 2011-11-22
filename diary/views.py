import datetime
import calendar
import logging
from collections import OrderedDict

import django.core.exceptions
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404

from cube.diary.models import Showing, Event, DiaryIdea

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def _get_date_range(year, month, day, user_days_ahead):
    if day is not None and month is None:
        raise Http404("Invalid request; cant specify day and no month")

    try:
        year = int(year) if year else None
        month = int(month) if month else None
        day = int(day) if day else None
    except ValueError:
        raise Http404("Invalid values")

    logger.debug("view_diary: day %s, month %s, year %s, span %s days", str(day), str(month), str(year), str(user_days_ahead))

    if day:
        startdate = datetime.date(year, month, day)
        days_ahead = 1
    elif month:
        startdate = datetime.date(year, month, 1)
        days_ahead = calendar.monthrange(year, month)[1]
    elif year:
        startdate = datetime.date(year, 1, 1)
        days_ahead = 365
        if calendar.isleap(year):
            days_ahead += 1 
    else:
        startdate = datetime.date.today()
        days_ahead = 30 # default

    if user_days_ahead:
        try:
            days_ahead = int(user_days_ahead)
        except (ValueError, TypeError):
            pass


    return startdate, days_ahead

def view_diary(request, year=None, month=None, day=None):
    context = { }
    query_days_ahead = request.GET.get('daysahead', None)
    startdate, days_ahead = _get_date_range(year, month, day, query_days_ahead)
    enddate = startdate + datetime.timedelta(days=days_ahead)

    context['today'] = datetime.date.today()
    context['start'] = startdate
    context['event_list_name'] = "Events for %s" % "/".join( [ str(s) for s in (day, month, year) if s ])
    # Do query:
    context['showings'] = Showing.objects.filter(confirmed=True).filter(hide_in_programme=False).filter(start__range=[startdate, enddate]).filter(event__private=False).order_by('start')

    return render_to_response('indexed_showing_list.html', context)

def edit_diary_list(request, year=None, day=None, month=None):
    context = { }
    # Sort out date range to display
    query_days_ahead = request.GET.get('daysahead', None)
    startdate, days_ahead = _get_date_range(year, month, day, query_days_ahead)
    enddate = startdate + datetime.timedelta(days=days_ahead)

    # Get all showings in the date range
    showings = Showing.objects.filter(start__range=[startdate, enddate]).order_by('start').select_related()
    # Build a dict with all the dates in the range as keys and empty lists as values
    dates = OrderedDict([ ((startdate + datetime.timedelta(days=days)), []) for days in xrange(days_ahead) ])
    # Put showings in the dict (so days without showings will have an empty dict)
    for showing in showings:
        dates[showing.start.date()].append(showing)

    # Get all 'ideas' in date range:
    idea_list = DiaryIdea.objects.filter(month__range=[startdate, enddate]).order_by('month').select_related()
    ideas = {}
    for idea in idea_list:
#        logging.info("%s: %s" % (str(idea), idea.ideas[0:50]))
        logging.info("%s: %s" % (str(idea), str(idea.ideas)))
        ideas[idea.month] = idea.ideas

    context['ideas'] = ideas
    context['dates'] = dates
    context['event_list_name'] = "Diary for %s to %s" % (str(startdate), str(enddate))
    context['start'] = startdate

    return render_to_response('edit_list.html', context)

def view_showing(request, showing_id=None):
    context = {}
    context['showing'] = get_object_or_404(Showing, id=showing_id)
    context['event'] = context['showing'].event
    return render_to_response('showing.html', context)

def view_event(request, event_id=None):
    context = {}
    context['event'] = get_object_or_404(Event, id=event_id)
    context['showings'] = context['event'].showing_set.all()
    return render_to_response('event.html', context)


