var Root = React.createClass({
    render: function () {
        return (
            <tbody>
            <tr>
                <td>1</td>
                <td>Lab Coat</td>
                <td>General</td>
                <td>40</td>
                <td><a href="/">EQ/1</a></td>
            </tr>
            <tr>
               <td>2</td>
                <td>Fundamental Calculus II</td>
                <td>Textbook</td>
                <td>8</td>
                <td><a href="/">EQ/2</a></td>
            </tr>
            <tr>
                <td>3</td>
                <td>TI84 Graphing Calculator</td>
                <td>General</td>
                <td>3</td>
                <td><a href="/">EQ/3</a></td>
            </tr>
            </tbody>
        );
    }
});

ReactDOM.render(<Root/>, document.getElementById("table"));
