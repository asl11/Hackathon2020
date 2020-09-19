
import React from 'react';

class Main extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            imageURL: '',
        };

        this.handleUploadImage = this.handleUploadImage.bind(this);
    }

    handleUploadImage(ev) {
        ev.preventDefault();

        const data = new FormData();
        data.append('file', this.uploadInput.files[0]);
        data.append('filename', this.fileName.value);

        fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: data,
        }).then((response) => {
            response.json().then((body) => {
                console.log(body);
                this.setState({ imageURL: `http://localhost:5000/${body.file}` });
            });
        });
    }

    render() {
        return (
            <form className="form-control-file" onSubmit={this.handleUploadImage}>
                <div>
                    <input className="btn" ref={(ref) => { this.uploadInput = ref; }} type="file" />
                </div>
                <br />
                <div>
                    <button className="btn btn-primary js-scroll-trigger">Run</button>
                </div>
            </form>


        );
    }
}

export default Main;
