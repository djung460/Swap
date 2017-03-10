var Root = React.createClass({
    getInitialState: function () {
        return {
            username: null,
            name: null,
            email: null,
            password: null,
            confirmPassword: null,
            phonenum: null,
            faculty: null,
            statesValue: null,
            forbiddenWords: ["password", "user", "username"]
        }
    },
    handleUsernameInput: function (event) {
        this.setState({
            username: event.target.value
        })
    },
    handleNameInput: function (event) {
        this.setState({
            name: event.target.value
        })
    },
    handlePhonenumInput: function (event) {
        this.setState({
            phonenum: event.target.value.replace(/(\d{3})\-?(\d{3})\-?(\d{4})/, '$1-$2-$3')
        })
    },
    handlePasswordInput: function (event) {
        if (!_.isEmpty(this.state.confirmPassword)) {
            this.regs.passwordConfirm.isValid();
        }
        this.regs.passwordConfirm.hideError();
        this.setState({
            password: event.target.value
        })
    },
    handleConfirmPasswordInput: function (event) {
        this.setState({
            confirmPassword: event.target.value
        })
    },
    isConfirmedPassword: function (event) {
        return event == this.state.password
    },
    handleSubmit: function (e) {
        e.preventDefault();
        $.ajax({
            url: "/api/auth/join",
            data: JSON.stringify({
                "username": this.state.formUsername,
                "password": this.state.formPassword,
                "email": this.state.formEmail,
                "name": this.state.formName,
                "phonenumber": this.state.formPhonenum,
                "year": this.state.formYear,
                "faculty": this.state.formFaculty
            }),
            method: 'PUT',
            success: function () {
                var newTitles = this.state.articleTitles;
                newTitles.push(this.state.formArticleTitle);
                this.setState({
                    formArticleTitle: "",
                    formArticleContent: "",
                    articleTitles: newTitles,
                });
            }.bind(this),
            error: function (err) {
                alert('Sorry! We are having trouble registering you!');
            }
        });
    },
    render: function () {
        return (
            <div className="create_account_screen">
            <form onSubmit={this.handleSubmit}>
                <div className="form-group">
                    <h4>
                        Username
                    </h4>
                    <input
                        text="Username"
                        ref="username"
                        validate={this.isEmpty}
                        value={this.state.username}
                        onChange={this.handleUsernameInput}
                        emptyMessage="Uername can't be empty"
                    />
                    <h4>
                        Name
                    </h4>
                    <input
                        text="Name"
                        ref="name"
                        validate={this.isEmpty}
                        value={this.state.name}
                        onChange={this.handleNameInput}
                        emptyMessage="Name can't be empty"
                    />
                    <h4>
                        Email
                    </h4>
                    <input
                        text="Email Address"
                        ref="email"
                        type="text"
                        defaultValue={this.state.email}
                        validate={this.validateEmail}
                        value={this.state.email}
                        onChange={this.handleEmailInput}
                        errorMessage="Email is invalid"
                        emptyMessage="Email can't be empty"
                        errorVisible={this.state.showEmailError}
                    />
                    <h4>
                        Enter Password
                    </h4>
                    <input
                        text="Password"
                        type="password"
                        ref="password"
                        validator="true"
                        minCharacters="8"
                        requireCapitals="1"
                        requireNumbers="1"
                        forbiddenWords={this.state.forbiddenWords}
                        value={this.state.passsword}
                        emptyMessage="Password is invalid"
                        onChange={this.handlePasswordInput}
                    />
                    <h4>
                        Confirm Password
                    </h4>
                    <input
                        text="Confirm password"
                        ref="passwordConfirm"
                        type="password"
                        validate={this.isConfirmedPassword}
                        value={this.state.confirmPassword}
                        onChange={this.handleConfirmPasswordInput}
                        emptyMessage="Please confirm your password"
                        errorMessage="Passwords don't match"
                    />
                    <h4>
                        Phone Number
                    </h4>
                    <input
                        text="Phone Number"
                        ref="phonenumber"
                        validate={this.isEmpty}
                        value={this.state.phonenumber}
                        onChange={this.handlePhonenumInput}
                        emptyMessage="Phone number can't be empty"
                    />
                    <h4>
                        Year
                    </h4>
                    <input
                        text="Year"
                        ref="year"
                        validate={this.isEmpty}
                        value={this.state.year}
                        onChange={this.handleYearInput}
                        emptyMessage="Year can't be empty"
                    />
                    <h4>
                        Faculty
                    </h4>
                    <input
                        text="Faculty"
                        ref="faculty"
                        validate={this.isEmpty}
                        value={this.state.faculty}
                        onChange={this.handleFacultyInput}
                        emptyMessage="Faculty can't be empty"
                    />

                    <button
                        type="submit"
                        className="button button_wide">
                        CREATE ACCOUNT
                    </button>
                </div>
            </form>
            </div>
        );
    }
});

ReactDOM.render(<Root/>, document.getElementById("page-content"));
