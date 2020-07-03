import React, {Fragment, useState} from 'react';
import uuid from 'uuid/v4';
import PropTypes from 'prop-types';

const FormSong = ({crearSong}) => {
    const [song, actualizarSong] = useState ({
        title: '',
        author: '',
        version: ''
    });

    const [error, setError] = useState(false);

    const handleChange = e => {
        actualizarSong({
            ...song,
            [e.target.name] : e.target.value
        })
    };

    const {title, author, version} = song;

    const submitSong = e => {
        e.preventDefault();

        if (title.trim() === '' || author.trim() === '' || version.trim() === '' ) {
            setError(true);
            return;
        }
        song.id = uui(); 

        crearSong(song);

        actualizarSong({
            title: '',
            author: '',
            version: ''
        })
    };

    return ( 
        <Fragment>
            <h2>Ingrese una cancion</h2>

            {error ? <p className=" alerta-error">Todos los campos son obligatorios</p> : null}

            <form onSubmit={submitSong}>
                <label>Nombre</label>
                <input type="text" name="title" className="u-full-width" onChange={handleChange} 
                       value={title} placeholder="Nombre de la cancion" />

                <label>Autor</label>
                <input type="text" name="author" className="u-full-width" onChange={handleChange} 
                    value={author} placeholder="Nombre del autor" />

                <label>Version</label>
                <input type="text" name="version" className="u-full-width" onChange={handleChange} 
                    value={version} placeholder="Nombre de la version" />

            <button type="submit" className="u-fill-width button-primary" >Agregar cancion</button>
            </form>
        </Fragment>
     );
}
FormSong.propTypes = {
    crearSong: PropTypes.func.isRequired
}
 
export default FormSong;