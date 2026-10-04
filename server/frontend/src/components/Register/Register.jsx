import React, { useState } from "react";
import Header from "../Header/Header";
import "./Register.css";

const Register = () => {
  const [form, setForm] = useState({
    userName: "", firstName: "", lastName: "", email: "", password: ""
  });
  const update = (event) => setForm({...form, [event.target.name]: event.target.value});
  const register = async (event) => {
    event.preventDefault();
    const response = await fetch("/djangoapp/register", {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify(form)
    });
    const result = await response.json();
    if (result.status === "Authenticated") {
      sessionStorage.setItem("username", result.userName);
      window.location.href = "/dealers";
    }
  };
  return <><Header/><form className="register-form" onSubmit={register}>
    <h1>Sign up</h1>
    <input name="userName" placeholder="Username" onChange={update} required />
    <input name="firstName" placeholder="First Name" onChange={update} required />
    <input name="lastName" placeholder="Last Name" onChange={update} required />
    <input name="email" type="email" placeholder="Email" onChange={update} required />
    <input name="password" type="password" placeholder="Password" onChange={update} required />
    <button type="submit">Register</button>
  </form></>;
};

export default Register;
