import React from 'react';
import PropTypes from 'prop-types';
import Button from '@material-ui/core/Button';
import withStyles from '@material-ui/core/styles/withStyles';

import '../styles/sign-up.css'

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200,
  },
  dense: {
    marginTop: 19,
  },
  menu: {
    width: 200,
  },
});


class SignupForm extends React.Component {
  state = {
    username: '',
    first_name: '',
    password: ''
  };

  handle_change = e => {
    const name = e.target.name;
    const value = e.target.value;
    this.setState(prevstate => {
      const newState = { ...prevstate };
      newState[name] = value;
      return newState;
    });
  };

  render() {
    const {component: Component, ...classes} = this.props.classes
    return (
      <div>
      <div className="container">
        <form onSubmit={e => this.props.handle_signup(e, this.state)}>
        <h4>Sign Up</h4>
        <label htmlFor="username">Username</label>
        <input
          type="text"
          name="username"
          value={this.state.username}
          onChange={this.handle_change}
        />
      <label htmlFor="first_name">First Name</label>
        <input
          type="text"
          name="first_name"
          value={this.state.first_name}
          onChange={this.handle_change}
        />
        <label htmlFor="password">Password</label>
        <input
          type="password"
          name="password"
          value={this.state.password}
          onChange={this.handle_change}
        />
        <input class="signup-button" type="submit" value="Complete Sign Up"/>
      </form>
    </div>
  </div>
    );
  }
}

export default withStyles(styles)(SignupForm)

SignupForm.propTypes = {
  handle_signup: PropTypes.func.isRequired
};
