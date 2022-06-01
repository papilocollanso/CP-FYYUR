"""
Artist, Venue and Show models
"""
# Imports

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

# Models.

class Venue(db.Model):
    """ Venue Model """
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String(120)))    # db.Array(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.String(), nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue', lazy=True)
    
    
    def to_dict(self):
        """ Returns a dictinary of venues """
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'genres': self.genres.split(','),  # convert string to list
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
        }  

    def __repr__(self):
      return f'<Venue {self.id}, {self.name}, {self.city}, {self.state},\
                {self.address}, {self.phone}, {self.genres},\
                {self.image_link}, {self.facebook_link},\
                {self.seeking_talent}, {self.seeking_description}>'


class Artist(db.Model):
    """ Artist Model"""
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate 
    genres = db.Column(db.ARRAY(db.String(120))) # db.Array(db.String(120))
    image_link = db.Column(db.String(500)) 
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.String(), nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy=True)
    
    def to_dict(self):
        """ Returns a dictinary of artists """
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'genres': self.genres.split(','),  # convert string to list
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
        }
    def __repr__(self):
          return f'<Artist {self.id}, {self.name}, {self.city}, {self.state},\
                {self.phone}, {self.genres}, {self.image_link},\
                {self.facebook_link}, {self.seeking_venue},\
                {self.seeking_description}>'
    
    
class Show(db.Model):
    """ Show Model """
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __repr__(self):
      return f'<Show artist_id: {self.artist_id} venue_id: {self.venue_id}\
             start_time: {self.start_time} venue: {self.venue.name}>'
             
    def show_venue(self):
        """ Returns a dictinary of venues for the show """
        return {
            'venue_id': self.venue_id,
            'venue_name': self.venue.name,
            'venue_image_link': self.venue.image_link,
            # convert datetime to string
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
    def show_artist(self):
        """ Returns a dictinary of artists for the show """
        return {
            'artist_id': self.artist_id,
            'artist_name': self.artist.name,
            'artist_image_link': self.artist.image_link,
            # convert datetime to string
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S')
        }
