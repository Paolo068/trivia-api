import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './stylesheets/App.css';
import FormView from './components/FormView';
import QuestionView from './components/QuestionView';
import Header from './components/Header';
import QuizView from './components/QuizView';

class App extends Component {
  render() {
    return (
      <div className='App'>
        <Header path />
        <Router>
          <Routes>
            <Route path='/' component={QuestionView} />
            <Route path='/add' component={FormView} />
            <Route path='/play' component={QuizView} />
            {/* <Route component={QuestionView} /> */}
          </Routes>
        </Router>
      </div>
    );
  }
}

export default App;
