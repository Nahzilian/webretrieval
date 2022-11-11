import './stylesheets/card.css'

const Card = (props) => {
    const {title, description} = props
    return (<div className='card-wrapper'>
        <div className='card'>
            <div className='card-title'>
                {title}
            </div>
            <div className='card-body'>
                {description}
            </div> 
        </div>
    </div>)
}

export default Card;