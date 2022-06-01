#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

"""
 Main file that starts the app
 Contains endpoints for the app
"""
from ast import Str
from asyncio.windows_events import NULL
from email.policy import default
import json
from xml.dom import NotFoundErr
import dateutil.parser
import babel
import sys
import os
from flask import Flask, render_template, request, Response, flash, redirect, url_for,abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import db, Artist, Venue, Show



#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
# db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/fyyur'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] =True  
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


  
   


   
   

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  areas = db.session.query(Venue.city, Venue.state).distinct(Venue.city, Venue.state)
  data=[]
  for area in areas:
    
  # Querying venues and filter them based on area (city, venue)
    result = Venue.query.filter(Venue.state == area.state).filter(Venue.city == area.city).all()

    venue_data = []

    # Creating venues' response
    for venue in result:
     venue_data.append({
     'id': venue.id,
     'name': venue.name,
     'num_upcoming_shows': len(db.session.query(Show).filter(Show.start_time > datetime.now()).all())
     })

     data.append({
     'city': area.city,
     'state': area.state,
     'venues': venue_data
     })
  return render_template('pages/venues.html', areas=data);
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  venues = db.session.query(Venue).filter(Venue.name.ilike('%' + search_term + '%')).all()
  # result = db.session.query(Artist).filter(Artist.name.ilike(f'%{search_term}%')).all()
  data = []

  for venue in venues:
      num_upcoming_shows = 0
      shows = db.session.query(Show).filter(Show.venue_id == venue.id)
      for show in shows:
          if (show.start_time > datetime.now()):
              num_upcoming_shows += 1;

      data.append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": num_upcoming_shows
      })

  response={
        "count": len(venues),
        "data": data
    }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
   venue = Venue.query.filter(Venue.id == venue_id).first()

   past = db.session.query(Show).filter(Show.venue_id == venue_id).filter(
   Show.start_time < datetime.now()).join(Artist, Show.artist_id == Artist.id).add_columns(Artist.id, Artist.name,
   Artist.image_link, Show.start_time).all()

   upcoming = db.session.query(Show).filter(Show.venue_id == venue_id).filter(
   Show.start_time > datetime.now()).join(Artist, Show.artist_id == Artist.id).add_columns(Artist.id, Artist.name,
   Artist.image_link, Show.start_time).all()

   upcoming_shows = []

   past_shows = []

   for i in upcoming:
      upcoming_shows.append({
        'artist_id': i[1],
        'artist_name': i[2],
        'image_link': i[3],
        'start_time': str(i[4])
        })

   for i in past:
         past_shows.append({
          'artist_id': i[1],
          'artist_name': i[2],
          'image_link': i[3],
          'start_time': str(i[4])
         })

   if venue is None:
          abort(404)

   data = {
        "id": venue.id,
        "name": venue.name,
        "genres": [venue.genres],
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past),
        "upcoming_shows_count": len(upcoming),
    }
   return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
   # TODO: insert form data as a new Venue record in the db, instead
   # TODO: modify data to be the data object returned from db insertion
   try:
       venue = Venue(
         name=request.form['name'],
         city=request.form['city'],
         state=request.form['state'],
         address=request.form['address'],
         phone=request.form['phone'],
         genres=request.form.getlist('genres'),
         image_link=request.form['image_link'],
         facebook_link=request.form['facebook_link'],
         website=request.form['website_link'],
         seeking_talent=request.form['seeking_talent'],
         seeking_description=request.form['seeking_description'])
       db.session.add(venue)
       db.session.commit()
         # on successful db insert, flash success
       flash('Venue ' + request.form['name'] + ' was successfully listed!')
        # TODO: on unsuccessful db insert, flash an error instead.
   except Exception as e:
       print(e)
       flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed')
       db.session.rollback()
       print(sys.exc_info())
   finally:
       db.session.close()
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
   return render_template('pages/home.html')

@app.route('/delete/<int:venue_id>', methods=['POST','GET'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        venue_to_delete = Venue.query.filter(Venue.id == venue_id)
        venue_to_delete.delete()
        db.session.commit()
        flash('Venue has been deleted successfully')
    except NotFoundErr:
        db.session.rollback()
        print(sys.ex_info())
        flash('Venue  was unsuccessfully deleted!')
        abort(404)
    finally:
        db.session.close()
    return render_template('pages/home.html')
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
   
   #  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
   search_term = request.form.get('search_term', '')
   result = db.session.query(Artist).filter(Artist.name.ilike(f'%{search_term}%')).all()
   count = len(result)
   response = {
    "count": count,
    "data": result
    }
   return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

   artist = Artist.query.filter(Artist.id == artist_id).first()

   past = db.session.query(Show).filter(Show.artist_id == artist_id).filter(
        Show.start_time < datetime.now()).join(Venue, Show.venue_id == Venue.id).add_columns(Venue.id, Venue.name,
        Venue.image_link,Show.start_time).all()

   upcoming = db.session.query(Show).filter(Show.artist_id == artist_id).filter(
        Show.start_time > datetime.now()).join(Venue, Show.venue_id == Venue.id).add_columns(Venue.id, Venue.name,
        Venue.image_link,Show.start_time).all()

   upcoming_shows = []

   past_shows = []

   for i in upcoming:
        upcoming_shows.append({
          'venue_id': i[1],
          'venue_name': i[2],
          'image_link': i[3],
          'start_time': str(i[4])
        })

   for i in past:
        past_shows.append({
            'venue_id':i[1],
            'venue_name':i[2],
            'image_link':i[3],
            'start_time':str(i[4])
        })

   if artist is None:
        abort(404)

   data = {
        "id": artist.id,
        "name": artist.name,
        "genres": [artist.genres],
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past),
        "upcoming_shows_count": len(upcoming),
    }
  
   return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
 # artist = Artist.query.filter(Artist.id == artist_id).first()
  # TODO: populate form with fields from artist with ID <artist_id>
    artist = Artist.query.get(artist_id)
    form = ArtistForm(
        name=artist.name,
        genres=artist.genres,
        city=artist.city,
        state=artist.state,
        phone=artist.phone,
        website_link=artist.website,
        facebook_link=artist.facebook_link,
        seeking_venue=artist.seeking_venue,
        seeking_description=artist.seeking_description,
        image_link=artist.image_link)
    
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    error = False
    try:
        artist = Artist.query.get(artist_id)
        artist.name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        artist.genres = ','.join(request.form.getlist('genres')),
        artist.website = request.form['website_link']
        artist.image_link = request.form['image_link']
        artist.facebook_link = request.form['facebook_link']
        artist.seeking_description = request.form['seeking_description']
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
        else:
            flash('Artist ' + request.form['name'] + ' was successfully updated!')  
    return redirect(url_for('show_artist', artist_id=artist_id))
      
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  form = VenueForm(
    name=venue.name,
    genres=venue.genres,
    address=venue.address,
    city=venue.city,
    state=venue.state,
    phone=venue.phone, 
    website_link=venue.website,
    facebook_link=venue.facebook_link,
    seeking_talent=venue.seeking_talent,
    seeking_description=venue.seeking_description,
    image_link=venue.image_link,)    
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  

    error = False
    try:
        venue = Venue.query.get(venue_id)
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        venue.genres = ','.join(request.form.getlist('genres')),                                      # convert list to string
        venue.facebook_link = request.form['facebook_link']
        venue.website = request.form['website_link']
        venue.image_link = request.form['image_link']
        venue.seeking_talent = request.form['seeking_talent']
        venue.seeking_description =request.form['seeking_description']
        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Venue ' +
                  request.form['name'] + ' could not be updated.')
        else:
            flash('Venue ' + request.form['name'] +
                  ' was successfully updated!')
        venue = Venue.query.get(venue_id)
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        venue.genres = ','.join(request.form.getlist('genres',type=str)),                                      # convert list to string
        venue.facebook_link = request.form['facebook_link']
        venue.website = request.form['website_link']
        venue.image_link = request.form['image_link']
        venue.seeking_talent = request.form['seeking_talent']
        venue.seeking_description =request.form['seeking_description']
        db.session.add(venue)
        db.session.commit()
        print(venue)
    return redirect(url_for('show_venue', venue_id=venue_id))
 

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['GET', 'POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  try:
   
    artist = Artist(
      name=request.form['name'],
      city=request.form['city'],
      state=request.form['state'],
      phone=request.form['phone'],
      genres=request.form.getlist('genres'),
      image_link=request.form['image_link'],
      facebook_link=request.form['facebook_link'],
      website=request.form['website_link'],
      seeking_venue=request.form['seeking_venue'], 
      seeking_description=request.form['seeking_description']) 
    db.session.add(artist)
    db.session.commit()
  
   
      # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
  except Exception as e:
    print(e)
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed!')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    
    db.session.close() 
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')

  

  


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
    shows = Show.query.all()

    data = []
    for show in shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": str(show.start_time)
        })
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
      
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  
  try:
    show = Show(
        artist_id=request.form['artist_id'],
        venue_id=request.form['venue_id'],
        start_time=request.form['start_time']) 
    db.session.add(show)
    db.session.commit()
        # on successful db insert, flash success
    flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  except Exception as e:
    print(e)
    flash('An error occurred. Show could not be listed!')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
"""if __name__ == '__main__':
    app.run()"""

# Or specify port manually:

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug = True)

