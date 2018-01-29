import React, { Component } from 'react';
import ListItem from './ListItem'



class ItemList extends Component {
    constructor(){
        super();
    }
    render() {
        let listItems = this.props.items.map(item => {
            return (<ListItem item={item} key={item.list_item_id}/>)
            }
        );
        return (
            <table className="List">
            <thead>
                <tr>
                    <th>Item Name</th>
                    <th>Item Description</th>
                    <th>Claim</th>
                </tr>
            </thead>
            <tbody>
                {listItems}
            </tbody>
            </table>
        );
    }
}



export default ItemList;