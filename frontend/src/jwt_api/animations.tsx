import {useState} from "react";
import styles_good_email from '@/styles/auth/CheckEmailAnimation.module.css';

const CheckEmailAnimation = ({onClose}: { onClose: () => void }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    const toggleExpand = () => {
        setIsExpanded(!isExpanded);
    };

    const handleOverlayClick = (e: React.MouseEvent<HTMLDivElement>) => {
        if (e.target === e.currentTarget) {
            onClose();
        }
    };

    return (
        <div className={styles_good_email.overlay} onClick={handleOverlayClick}>
            <div className={styles_good_email.modal}>
                <div className={styles_good_email.message}>Проверьте свой почтовый ящик</div>
                <div className={styles_good_email.arrowContainer} onClick={toggleExpand}>
                    <div className={styles_good_email.arrowText}>Я не вижу Email</div>
                    <div
                        className={`${styles_good_email.arrow} ${isExpanded ? styles_good_email.arrowUp : styles_good_email.arrowDown}`}></div>
                </div>
                {isExpanded && (
                    <div className={styles_good_email.additionalMessage}>
                        Проверьте спам
                    </div>
                )}
            </div>
        </div>
    );
};

export default CheckEmailAnimation;