"""
Python  API for the playlist service.
"""

# Standard library modules

# Installed packages
import requests


class playlist():
    """Python API for the playlist service.

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the music service. Often
        'http://cmpt756s2:30001/'. Note the trailing slash.
    auth: string
        Authorization code to pass to the music service. For many
        implementations, the code is required but its content is
        ignored.
    """
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def create(self, pl_name, song):
        """Create an artist, song pair.

        Parameters
        ----------
        artist: string
            The artist performing song.
        song: string
            The name of the song.

        Returns
        -------
        (number, string)
            The number is the HTTP status code returned by Music.
            The string is the UUID of this song in the music database.
        """
        r = requests.post(
            self._url,
            json={'Artist': pl_name,
                  'SongTitle': song},
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['playlist_id']

    def add(self, pl_id, music_id):
        r = requests.put(
            self._url + 'add_to_list/' + pl_id,
            json={"music_id" : music_id},
            headers={'Authorization': self._auth}
            )
        return r.status_code

    def delete_song(self, pl_id, music_id):
        """Delete an artist, song pair.

        Parameters
        ----------
        m_id: string
            The UUID of this song in the music database.

        Returns
        -------
        Does not return anything. The music delete operation
        always returns 200, HTTP success.
        """
        r = requests.put(
            self._url + 'delete_from_list/' + pl_id,
            json={'music_id' : music_id},
            headers={'Authorization': self._auth}
        )
        return r.status_code
    
    def read(self, pl_id):
        """Read an playlist

        Parameters
        ----------
        m_id: string
            The UUID of this song in the music database.

        Returns
        -------
        status, artist, title

        status: number
            The HTTP status code returned by Music.
        artist: If status is 200, the artist performing the song.
          If status is not 200, None.
        title: If status is 200, the title of the song.
          If status is not 200, None.
        """
        r = requests.get(
            self._url + pl_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None, None

        item = r.json()['Items'][0]
        return r.status_code, item['listname'], item['SongTitle']

    def delete(self, pl_id):
        """Delete an playlist

        Parameters
        ----------
        m_id: string
            The UUID of this song in the music database.

        Returns
        -------
        Does not return anything. The music delete operation
        always returns 200, HTTP success.
        """
        requests.delete(
            self._url + pl_id,
            headers={'Authorization': self._auth}
        )