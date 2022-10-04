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
            <Route path='/' element={<QuestionView/>} exact />
            <Route path='/add' element={<FormView/>} exact />
            <Route path='/play' element={<QuizView/>} exact />
            <Route element={<QuestionView/>} />
          </Routes>
        </Router>
      </div>
    );
  }
}

export default App;
