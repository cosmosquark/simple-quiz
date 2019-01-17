import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import Button from '@material-ui/core/Button'
import styles from '../styles/material-ui/styles'

function Nav(props) {
  const {component: Component, ...classes} = props.classes;
  const logged_out_nav = (
    <div>
      <div className={classes.root}>
        <AppBar position="static">
          <Toolbar>
            <Button color="inherit" className={classes.navlink} onClick={() => props.display_form('login')}>Login</Button>
            <Button color="inherit" className={classes.navlink} onClick={() => props.display_form('signup')}>Sign Up</Button>
              <div class="title">
                  The Maths Quiz
              </div>
            <div class="user-info">
                Please Log In
            </div>
          </Toolbar>
        </AppBar>
      </div>
    </div>
  );

  const logged_in_nav = (
    <div>
      <div className={classes.root}>
        <AppBar position="static">
          <Toolbar>
            <Button color="inherit" className={classes.navlink} onClick={props.handle_logout}>Logout</Button>
              <div class="title">
                  The Maths Quiz
              </div>
              <div class="user-info">
                Hello {props.username}
              </div>
          </Toolbar>
        </AppBar>
      </div>
    </div>

  )
  return <div>{props.logged_in ? logged_in_nav : logged_out_nav}</div>;
}

/*
function Nav(props) {
  const logged_out_nav = (
    <ul>
      <li onClick={() => props.display_form('login')}>login</li>
      <li onClick={() => props.display_form('signup')}>signup</li>
    </ul>
  );

  const logged_in_nav = (
    <ul>
      <li onClick={props.handle_logout}>logout</li>
    </ul>
  );
  return <div>{props.logged_in ? logged_in_nav : logged_out_nav}</div>;
}
*/

export default withStyles(styles)(Nav)

Nav.propTypes = {
  logged_in: PropTypes.bool.isRequired,
  display_form: PropTypes.func.isRequired,
  handle_logout: PropTypes.func.isRequired,
  classes: PropTypes.object.isRequired
};
