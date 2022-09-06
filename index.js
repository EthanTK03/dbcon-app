import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import axios from 'axios';

class Main extends React.Component {
    constructor() {
        super()
        this.state = {user: null, usercount: 0, totalcount: 0}
    }
    onLoginChange(e) {
        this.setState({...this.state, user: e.target.value})
    }
    login() {
        const {user} = this.state
        var url = 'http://127.0.0.1:5000/login/' + user
        axios.get(url).then((resp) => {
            this.setState({...this.state, 
                usercount: resp.data['user count'], 
                totalcount: resp.data['total count']
            })
        }).catch(error => {
            console.log(error)
        })
        
    }
        
    render() {
        const {user, usercount, totalcount} = this.state
        return (
            <div className='Main'>
                <p>
                    <span>login: </span><input value={user} onChange={this.onLoginChange.bind(this)}/>
                    <button onClick={this.login.bind(this)}>Login</button>
                </p>
                {(usercount > 0) && 
                <div>
                    <p><span>{user} count: {usercount}</span></p>
                    <p><span>total count: {totalcount}</span></p>
                </div>
                }
            </div>
        )
    }
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Main />);