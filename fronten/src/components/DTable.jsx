import React from 'react';
import MaterialTable from "material-table";

export default class DTable extends React.Component {

    constructor(props){
        super(props);
        this.getHeader = this.getHeader.bind(this);
        this.getRowsData = this.getRowsData.bind(this);
        this.getKeys = this.getKeys.bind(this);
    }

    getKeys = function(){
        return Object.keys(this.props.data[0]);
    }

    getHeader = function(){
        var keys = this.getKeys();
        return keys.map((key, index)=>{
            return <th key={key}>{key.toUpperCase()}</th>
        })
    }

    getRowsData = function(){
        var items = this.props.data;
        var keys = this.getKeys();
        return items.map((row, index)=>{
            return <tr key={index}><RenderRow key={index} data={row} keys={keys}/></tr>
        })
    }

    render() {
        return (
            <div style={{ maxWidth: "100%" }}>
                <MaterialTable
                    columns={[
                        { title: "Meeting ID", field: "MeetingID" },
                        { title: "Meeting Time", field: "MeetingTime" },
                        { title: "Assigned Room", field: "AssignedRoom"},
                        { title: "Number of Attendees", field:"NumberofAttendees", type:"numeric"},
                        { title: "Score", field:"Score", type:"numeric"}

                    ]}
                    data={this.props.data}
                    title="Model Results"
                />
            </div>
        );
        {/*return (
            <div>
                <table>
                    <thead>
                    <tr>{this.getHeader()}</tr>
                    </thead>
                    <tbody>
                    {this.getRowsData()}
                    </tbody>
                </table>
            </div>

        );*/}
    }
}
const RenderRow = (props) =>{
    return props.keys.map((key, index)=>{
        return <td key={props.data[key]}>{props.data[key]}</td>
    })
}