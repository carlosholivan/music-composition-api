<div>
<img style="float:left; border-radius:50%" src="https://avatars2.githubusercontent.com/u/58553327?s=460&u=3276252f07fb379c248bc8c9ce344bfdcaed7c45&v=4" width="40px">
</div>
<br>


Music Composition API, A collection of Deep Learning for Music Generation models deployed as an API with Flask.

## TODOs

- [ ] Test models
- [ ] Put music2score in werbserver to be able to print a score of a MIDI file
- [ ] Reorganize musicvae.py code
- [ ] Add more musicVAE checkpoints for inference (trios...)
- [ ] Add Music Transformer model
- [ ] Add MMM model

## Documentation

The docs will be released as soon as the pakage version is stable.


## Dependencies

* [Magenta](https://github.com/magenta/magenta)
* [VisualMIDI](https://github.com/dubreuia/visual_midi)
* [pretty MIDI](https://github.com/craffel/pretty-midi)
* [music21](https://github.com/cuthbertLab/music21)
* [Flask cors]()
* [Coverage]()


## Package Structure

[*models/*](models/)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;module containing the code of all the music generation models.

[*checkpoints/*](checkpoints/)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;model's checkpoints to perform inference.

[*notebooks/*](notebooks/)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;tutorial notebooks.

[*tests/*](tests/)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;unittests.

[*examples/*](examples/)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;examples obtained with this package.


## Development

### Conda dev environment

Using conda to setup a dev environment by running

`conda env update -f environment.yml`

In order to activate this environment you will need to running

`conda activate music-composition-api`

### Pip
This package is still in development. To install the current version, clone this repository and run:


`cd path-of-this-package`

`pip install -e .`

### Testing

To run tests: `pytest tests/`


## API Commands
Sending a command to the webserver: `POST /api/command`

It must include a payload:

```
{
	"command_name": "..."
}
```

Where `commmand_name` is the name of the command.


### Commands.

#### MusicVAE.

```
{
    "command_name": "music_vae"
}
```

## Authors

[**Carlos Hernández-Oliván**](https://carlosholivan.github.io/index.html) (PhD Candidate) - carloshero@unizar.es

**Jorge Abadías Puyuelo** (Bachelor Thesis student)

Department of Electronic Engineering and Communications, Universidad de Zaragoza.
