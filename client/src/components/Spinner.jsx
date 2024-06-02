import ClipLoader from 'react-spinners/ClipLoader';

const override = {
	display: 'block',
	margin: '100px auto',
};

const Spinner = ({ loading }) => {
	return (
		<ClipLoader
			color='#4338ca'
			loading={loading}
			cssOverride={override}
			size={50}
		/>
	);
};

export default Spinner;
