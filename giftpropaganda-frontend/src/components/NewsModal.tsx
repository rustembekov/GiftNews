import React, { useEffect } from 'react';
import styled from 'styled-components';
import MediaViewer from './MediaViewer';
import TelegramWebApp from '../telegram/TelegramWebApp';
import DOMPurify from 'dompurify';
import { NewsItem } from '../types';
import { formatTimeAgo } from '../utils/formatters';

interface NewsModalProps {
    news: NewsItem;
    isOpen: boolean;
    onClose: () => void;
}

const ModalOverlay = styled.div<{ $isOpen: boolean }>`
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.9);
    backdrop-filter: blur(10px);
    z-index: 1000;
    opacity: ${props => props.$isOpen ? 1 : 0};
    visibility: ${props => props.$isOpen ? 'visible' : 'hidden'};
    transition: all 0.3s ease;
`;

const ModalContainer = styled.div<{ $isOpen: boolean }>`
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background: var(--tg-theme-bg-color, #0f0f0f);
    color: var(--tg-theme-text-color, #ffffff);
    transform: translateY(${props => props.$isOpen ? '0' : '100%'});
    transition: transform 0.3s ease;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
`;

const ModalHeader = styled.div`
    position: sticky;
    top: 0;
    background: var(--tg-theme-bg-color, #0f0f0f);
    padding: 12px 16px;
    border-bottom: 1px solid var(--tg-theme-hint-color, #333);
    backdrop-filter: blur(10px);
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: space-between;
`;

const BackButton = styled.button`
    background: none;
    border: none;
    color: var(--tg-theme-button-color, #0088cc);
    font-size: 16px;
    cursor: pointer;
    padding: 8px;
    margin: -8px;
    border-radius: 6px;
    transition: background 0.2s ease;

    &:hover {
        background: var(--tg-theme-secondary-bg-color, #1a1a1a);
    }
`;

const ShareButton = styled.button`
    background: none;
    border: none;
    color: var(--tg-theme-text-color, #ffffff);
    font-size: 16px;
    cursor: pointer;
    padding: 8px;
    margin: -8px;
    border-radius: 6px;
    transition: background 0.2s ease;

    &:hover {
        background: var(--tg-theme-secondary-bg-color, #1a1a1a);
    }
`;

const ModalContent = styled.div`
    flex: 1;
    padding: 0 12px 40px 12px;
    max-width: 100%;
    margin: 0 auto;
    width: 100%;
    
    @media (min-width: 768px) {
        padding: 0 16px 40px 16px;
        max-width: 800px;
    }
`;

const ArticleHeader = styled.div`
    margin: 20px 0;
`;

const CategoryBadge = styled.span`
    display: inline-block;
    padding: 4px 8px;
    background: var(--tg-theme-button-color, #0088cc);
    color: var(--tg-theme-button-text-color, #ffffff);
    border-radius: 4px;
    font-size: 11px;
    font-weight: 500;
    margin-bottom: 12px;
`;

const ArticleTitle = styled.h1`
    font-size: 24px;
    font-weight: 700;
    line-height: 1.3;
    margin: 0 0 16px 0;
    color: var(--tg-theme-text-color, #ffffff);
`;

const ArticleSubtitle = styled.p`
    font-size: 16px;
    line-height: 1.5;
    color: var(--tg-theme-hint-color, #999);
    margin: 0 0 20px 0;
`;

const ArticleMeta = styled.div`
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 24px;
    font-size: 13px;
    color: var(--tg-theme-hint-color, #888);
    flex-wrap: wrap;
`;

const MetaItem = styled.span`
    display: flex;
    align-items: center;
    gap: 4px;
`;

const ArticleContent = styled.div`
    font-size: 16px;
    line-height: 1.7;
    color: var(--tg-theme-text-color, #ffffff);
    margin: 24px 0;
    padding: 20px;
    background: var(--tg-theme-secondary-bg-color, #1a1a1a);
    border-radius: 12px;
    border: 1px solid var(--tg-theme-hint-color, #333);
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
    overflow: hidden;
    word-wrap: break-word;

    p {
        margin: 0 0 16px 0;
        text-align: justify;
        hyphens: auto;
    }

    p:last-child {
        margin-bottom: 0;
    }

    h2, h3, h4 {
        margin: 24px 0 12px 0;
        color: var(--tg-theme-text-color, #ffffff);
        font-weight: 600;
    }

    h2 {
        font-size: 20px;
        border-bottom: 2px solid var(--tg-theme-button-color, #0088cc);
        padding-bottom: 8px;
    }

    h3 {
        font-size: 18px;
    }

    h4 {
        font-size: 16px;
    }

    ul, ol {
        margin: 0 0 16px 0;
        padding-left: 20px;
    }

    li {
        margin-bottom: 8px;
    }

    blockquote {
        margin: 16px 0;
        padding: 16px 20px;
        background: rgba(0, 136, 204, 0.1);
        border-left: 4px solid var(--tg-theme-button-color, #0088cc);
        border-radius: 0 8px 8px 0;
        font-style: italic;
    }

    code {
        background: var(--tg-theme-secondary-bg-color, #1a1a1a);
        padding: 4px 8px;
        border-radius: 6px;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 14px;
        border: 1px solid var(--tg-theme-hint-color, #333);
    }

    pre {
        background: var(--tg-theme-secondary-bg-color, #1a1a1a);
        padding: 16px;
        border-radius: 8px;
        overflow-x: auto;
        border: 1px solid var(--tg-theme-hint-color, #333);
        margin: 16px 0;
    }

    pre code {
        background: none;
        padding: 0;
        border: none;
    }

    strong, b {
        font-weight: 600;
        color: var(--tg-theme-button-color, #0088cc);
    }

    em, i {
        font-style: italic;
        color: var(--tg-theme-hint-color, #999);
    }

    a {
        color: var(--tg-theme-button-color, #0088cc);
        text-decoration: none;
        border-bottom: 1px solid var(--tg-theme-button-color, #0088cc);
    }

    a:hover {
        text-decoration: underline;
    }

    img {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        margin: 16px 0;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0;
        background: var(--tg-theme-secondary-bg-color, #1a1a1a);
        border-radius: 8px;
        overflow: hidden;
    }

    th, td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid var(--tg-theme-hint-color, #333);
    }

    th {
        background: var(--tg-theme-button-color, #0088cc);
        color: var(--tg-theme-button-text-color, #ffffff);
        font-weight: 600;
    }

    @media (max-width: 768px) {
        font-size: 15px;
        padding: 16px;
        margin: 16px 0;
    }
`;

const InteractionBar = styled.div`
    margin-top: 32px;
    padding: 16px 0;
    border-top: 1px solid var(--tg-theme-hint-color, #333);
    display: flex;
    align-items: center;
    justify-content: space-between;
`;

const InteractionButtons = styled.div`
    display: flex;
    gap: 20px;
`;

const InteractionButton = styled.button`
    background: none;
    border: none;
    color: var(--tg-theme-hint-color, #888);
    font-size: 14px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 12px;
    border-radius: 6px;
    transition: all 0.2s ease;

    &:hover {
        background: var(--tg-theme-secondary-bg-color, #1a1a1a);
        color: var(--tg-theme-text-color, #ffffff);
    }

    &.active {
        color: var(--tg-theme-button-color, #0088cc);
    }
`;



const DescriptionSection = styled.div`
    margin: 24px 0;
    padding: 16px;
    background: var(--tg-theme-secondary-bg-color, #1a1a1a);
    border-radius: 12px;
    border: 1px solid var(--tg-theme-hint-color, #333);
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
    overflow: hidden;
    word-wrap: break-word;
    
    @media (min-width: 768px) {
        padding: 20px;
    }
`;

const DescriptionTitle = styled.h3`
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 16px 0;
    color: var(--tg-theme-text-color, #ffffff);
`;

const LinksContainer = styled.div`
    display: flex;
    flex-direction: column;
    gap: 12px;
    width: 100%;
    max-width: 100%;
`;

const LinkItem = styled.a`
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--tg-theme-button-color, #0088cc);
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    padding: 8px 12px;
    background: rgba(0, 136, 204, 0.1);
    border-radius: 8px;
    transition: all 0.2s ease;
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
    overflow: hidden;
    word-wrap: break-word;

    &:hover {
        background: rgba(0, 136, 204, 0.2);
        transform: translateY(-1px);
    }
`;

const LinkIcon = styled.span`
    font-size: 16px;
`;

const LinkText = styled.span`
    flex: 1;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
`;

const HighlightText = styled.span`
    color: #ff6b6b;
    font-weight: 600;
`;

const ImportantNotice = styled.div`
    margin-top: 16px;
    padding: 12px;
    background: rgba(255, 107, 107, 0.1);
    border: 1px solid rgba(255, 107, 107, 0.3);
    border-radius: 8px;
    font-size: 14px;
    line-height: 1.5;
    color: var(--tg-theme-text-color, #ffffff);
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
    overflow: hidden;
    word-wrap: break-word;
`;

const SourceInfo = styled.div`
  margin-top: 20px;
  font-size: 14px;
  color: var(--tg-theme-hint-color, #888);
`;

const NewsModal: React.FC<NewsModalProps> = ({news, isOpen, onClose}) => {
    useEffect(() => {
        if (isOpen) {
            document.body.style.overflow = 'hidden';
            TelegramWebApp.expand();
        } else {
            document.body.style.overflow = 'auto';
        }

        return () => {
            document.body.style.overflow = 'auto';
        };
    }, [isOpen]);

    useEffect(() => {
        const handleEscape = (e: KeyboardEvent) => {
            if (e.key === 'Escape') {
                onClose();
            }
        };

        if (isOpen) {
            document.addEventListener('keydown', handleEscape);
        }

        return () => {
            document.removeEventListener('keydown', handleEscape);
        };
    }, [isOpen, onClose]);

    const handleBackClick = () => {
        TelegramWebApp.triggerHapticFeedback('impact');
        onClose();
    };

    const handleShare = () => {
        TelegramWebApp.triggerHapticFeedback('impact');
        if (navigator.share) {
            navigator.share({
                title: news.title,
                text: news.content.substring(0, 200) + '...',
                url: news.link
            });
        }
    };

    const handleInteraction = (type: string) => {
        TelegramWebApp.triggerHapticFeedback('impact');
    };

    const createMarkup = (html: string) => {
        return {
            __html: DOMPurify.sanitize(html, {
                ALLOWED_TAGS: [
                    'p', 'br', 'strong', 'b', 'em', 'i', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                    'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
                    'div', 'span', 'mark', 'del', 'ins', 'sub', 'sup'
                ],
                ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'target', 'rel', 'class', 'id', 'style'],
                ALLOWED_URI_REGEXP: /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i
            })
        };
    };

    return (
        <ModalOverlay $isOpen={isOpen} onClick={onClose}>
            <ModalContainer $isOpen={isOpen} onClick={(e) => e.stopPropagation()}>
                <ModalHeader>
                    <BackButton onClick={handleBackClick}>← Назад</BackButton>
                    <ShareButton onClick={handleShare}>📤</ShareButton>
                </ModalHeader>

                <ModalContent>
                    <ArticleHeader>
                        <CategoryBadge>{news.category.toUpperCase()}</CategoryBadge>
                        <ArticleTitle>{news.title}</ArticleTitle>
                        {news.subtitle && <ArticleSubtitle>{news.subtitle}</ArticleSubtitle>}

                        <ArticleMeta>
                            {news.author && <MetaItem>👤 {news.author}</MetaItem>}
                            <MetaItem>🕒 {formatTimeAgo(news.publish_date)}</MetaItem>
                            {news.reading_time && (
                                <MetaItem>📖 {news.reading_time} мин чтения</MetaItem>
                            )}
                            {news.views_count !== undefined && (
                                <MetaItem>👁️ {news.views_count} просмотров</MetaItem>
                            )}
                        </ArticleMeta>
                    </ArticleHeader>

                    {news.media && news.media.length > 0 && (
                        <div style={{ marginBottom: '20px' }}>
                            {news.media.map((mediaItem, index) => (
                                <MediaViewer key={index} mediaItem={mediaItem}/>
                            ))}
                        </div>
                    )}

                    {news.content_html && (
                        <ArticleContent dangerouslySetInnerHTML={createMarkup(news.content_html)}/>
                    )}
                    {!news.content_html && news.content && (
                        <ArticleContent>
                            {news.content.split('\n\n').map((paragraph, index) => (
                                <p key={index}>{paragraph.trim()}</p>
                            ))}
                        </ArticleContent>
                    )}
                    {!news.content_html && !news.content && (
                        <ArticleContent>
                            <p style={{ textAlign: 'center', color: 'var(--tg-theme-hint-color, #999)' }}>
                                📄 Контент статьи загружается...
                            </p>
                        </ArticleContent>
                    )}

                    {/* Описание с ссылками */}
                    <DescriptionSection>
                        <DescriptionTitle>📋 Полезные ссылки</DescriptionTitle>
                        
                        <LinksContainer>
                            <LinkItem href="https://t.me/source" target="_blank" rel="noopener noreferrer">
                                <LinkIcon>💡</LinkIcon>
                                <LinkText>Источник</LinkText>
                            </LinkItem>
                            
                            <LinkItem href="https://t.me/nft_chat" target="_blank" rel="noopener noreferrer">
                                <LinkIcon>🚀</LinkIcon>
                                <LinkText>Чат для покупки/продажи NFT</LinkText>
                            </LinkItem>
                            
                            <LinkItem href="https://t.me/portals" target="_blank" rel="noopener noreferrer">
                                <LinkIcon>❤️</LinkIcon>
                                <LinkText>Portals ❤️</LinkText>
                            </LinkItem>
                        </LinksContainer>

                        <ImportantNotice>
                            <HighlightText>‼️ На Portals теперь доступны розыгрыши!</HighlightText>
                            <br />
                            Запустить розыгрыш вы можете перейдя во вкладку профиль, а потом giveaways.
                        </ImportantNotice>
                    </DescriptionSection>

                    {news.source?.name && (
                        <SourceInfo>
                            Источник:{" "}
                            {news.source?.name}
                        </SourceInfo>
                    )}

                    <InteractionBar>
                        <InteractionButtons>
                            <InteractionButton onClick={() => handleInteraction('like')}>
                                🔥 +2
                            </InteractionButton>
                            <InteractionButton onClick={() => handleInteraction('comment')}>
                                💬 0
                            </InteractionButton>
                            <InteractionButton onClick={() => handleInteraction('bookmark')}>
                                🔖 3
                            </InteractionButton>
                        </InteractionButtons>
                    </InteractionBar>
                </ModalContent>
            </ModalContainer>
        </ModalOverlay>
    );
};

export default NewsModal;
