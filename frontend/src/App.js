import React, { useState, useEffect, Fragment } from 'react';
import Song from './components/Song';
import FormSong from './components/FormSong';



function App() {

  // const [currentTime, setCurrentTime] = useState(0);

  // useEffect(() => {
  //   fetch('/time').then(res => res.json()).then(data => {
  //     setCurrentTime(data.time);
  //   });
  // }, []);

  

  const [mysongs, handlermySongs] = useState([]);
  useEffect(() => {
    fetch('/code/api/v1.0/songs').then(res => res.json()).then(data => {
      handlermySongs(data['data']);
    });
  }, []);


  let songsInit = JSON.parse(localStorage.getItem('songs'));
  if( !songsInit) {
    songsInit = [];
  }

  const [songs, handleCitas] = useState(songsInit);
  
  useEffect( () => {
    let songsInit = JSON.parse(localStorage.getItem('songs'));
    if( songsInit) {
      localStorage.setItem('songs', JSON.stringify(songs))
    }else {
      localStorage.setItem('songs', JSON.stringify([]));
    }
  }, [songs]);// pasamos el array vacío para que no se cicle cuando api, cada que cambie el state de songs se exe

  //funcion que tomará las songs actuales y agregará la nueva
  const crearSong = song => {
    handleCitas([
      ...songs,
      song
    ]);
    // aqui incluire mi metodo post de flask
  }
  const eliminarSong = id => {
    const nuevoSong = songs.filter( song => song.id !== id);
    handleCitas(nuevoSong)
  }
  const titulo = songs.length === 0 ? 'No Hay Canciones' : 'Administra tus Canciones';

  return (
    <Fragment >
      <h1>Canciones diarias</h1>
      <div className="container">
        <div className="row">
          <div className="one-half column">
            <FormSong crearSong={crearSong} />
          </div>
          <div className="one-half column">
            <h2>{titulo}</h2>
            { songs.map( song => (
                <Song key={song.id} song={song} eliminarSong={eliminarSong} />
              ))
            }
            { mysongs.map( mysong => (
              <Song key={mysong.id} song={mysong}  />
            ))
            }
          </div>
        </div>
      </div>
    </Fragment>
    
  );
}

export default App;
