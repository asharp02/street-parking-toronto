function BylawToggle() {
    return (
        <div className="toggleSidebar">
            <div className="toggleOption">
                <input type="checkbox" id="noParking" name="noParking" value="noParking" checked></input>
                <label for="noParking">No Parking</label>
            </div>
            <div className="toggleOption">
                <input type="checkbox" id="validParking" name="validParking" value="validParking" checked></input>
                <label for="validParking">Valid Parking</label>
            </div>
        </div>
    )
}

export default BylawToggle;