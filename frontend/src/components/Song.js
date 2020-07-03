import React from 'react';
import PropTypes from 'prop-types';

const Song = ({song, eliminarSong}) => (
    <div className="song">
        <p>Nombre: <span>{song.title}</span></p>
        <p>Autor: <span>{song.author}</span></p>
        <p>Version: <span>{song.version}</span></p>

        <button className="button u-fill-width eliminar" onClick={ () => eliminarSong(song.id)}>eliminar &times;</button>
    </div>
);

Song.propTypes = {
    song: PropTypes.object.isRequired,
    eliminarSong: PropTypes.object.isRequired
}
 
export default Song;