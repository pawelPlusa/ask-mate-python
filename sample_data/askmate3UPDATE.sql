--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2
-- Dumped by pg_dump version 12.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: answer; Type: TABLE; Schema: public; Owner: Tomek
--

CREATE TABLE public.answer (
    id integer NOT NULL,
    submission_time timestamp without time zone NOT NULL,
    vote_number integer DEFAULT 0 NOT NULL,
    question_id integer NOT NULL,
    message text NOT NULL,
    image text,
    user_id integer,
    accepted boolean DEFAULT false NOT NULL
);


ALTER TABLE public.answer OWNER TO "Tomek";

--
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: Tomek
--

CREATE SEQUENCE public.answer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.answer_id_seq OWNER TO "Tomek";

--
-- Name: answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Tomek
--

ALTER SEQUENCE public.answer_id_seq OWNED BY public.answer.id;


--
-- Name: comment; Type: TABLE; Schema: public; Owner: Tomek
--

CREATE TABLE public.comment (
    id integer NOT NULL,
    question_id integer,
    answer_id integer,
    message text NOT NULL,
    submission_time timestamp without time zone NOT NULL,
    edited_count integer DEFAULT 0 NOT NULL,
    user_id integer,
    CONSTRAINT question_answer_ids_ecxlusion CHECK (((question_id IS NULL) OR (answer_id IS NULL)))
);


ALTER TABLE public.comment OWNER TO "Tomek";

--
-- Name: comment_id_seq; Type: SEQUENCE; Schema: public; Owner: Tomek
--

CREATE SEQUENCE public.comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comment_id_seq OWNER TO "Tomek";

--
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Tomek
--

ALTER SEQUENCE public.comment_id_seq OWNED BY public.comment.id;


--
-- Name: question; Type: TABLE; Schema: public; Owner: Tomek
--

CREATE TABLE public.question (
    id integer NOT NULL,
    submission_time timestamp without time zone NOT NULL,
    view_number integer DEFAULT 0 NOT NULL,
    vote_number integer DEFAULT 0 NOT NULL,
    title text NOT NULL,
    message text NOT NULL,
    image text,
    user_id integer
);


ALTER TABLE public.question OWNER TO "Tomek";

--
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: Tomek
--

CREATE SEQUENCE public.question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.question_id_seq OWNER TO "Tomek";

--
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Tomek
--

ALTER SEQUENCE public.question_id_seq OWNED BY public.question.id;


--
-- Name: question_tag; Type: TABLE; Schema: public; Owner: Tomek
--

CREATE TABLE public.question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.question_tag OWNER TO "Tomek";

--
-- Name: tag; Type: TABLE; Schema: public; Owner: Tomek
--

CREATE TABLE public.tag (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.tag OWNER TO "Tomek";

--
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: Tomek
--

CREATE SEQUENCE public.tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tag_id_seq OWNER TO "Tomek";

--
-- Name: tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Tomek
--

ALTER SEQUENCE public.tag_id_seq OWNED BY public.tag.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: Tomek
--

CREATE TABLE public.users (
    id integer NOT NULL,
    login text NOT NULL,
    password text NOT NULL,
    user_name text NOT NULL,
    registration_date timestamp without time zone NOT NULL,
    reputation integer DEFAULT 0 NOT NULL,
    inactive boolean DEFAULT false
);


ALTER TABLE public.users OWNER TO "Tomek";

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: Tomek
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO "Tomek";

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Tomek
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: answer id; Type: DEFAULT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.answer ALTER COLUMN id SET DEFAULT nextval('public.answer_id_seq'::regclass);


--
-- Name: comment id; Type: DEFAULT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.comment ALTER COLUMN id SET DEFAULT nextval('public.comment_id_seq'::regclass);


--
-- Name: question id; Type: DEFAULT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.question ALTER COLUMN id SET DEFAULT nextval('public.question_id_seq'::regclass);


--
-- Name: tag id; Type: DEFAULT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.tag ALTER COLUMN id SET DEFAULT nextval('public.tag_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: Tomek
--

COPY public.answer (id, submission_time, vote_number, question_id, message, image, user_id, accepted) FROM stdin;
\.


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: Tomek
--

COPY public.comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) FROM stdin;
\.


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: Tomek
--

COPY public.question (id, submission_time, view_number, vote_number, title, message, image, user_id) FROM stdin;
\.


--
-- Data for Name: question_tag; Type: TABLE DATA; Schema: public; Owner: Tomek
--

COPY public.question_tag (question_id, tag_id) FROM stdin;
\.


--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: Tomek
--

COPY public.tag (id, name) FROM stdin;
1	python
2	sql
3	css
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: Tomek
--

COPY public.users (id, login, password, user_name, registration_date, reputation, inactive) FROM stdin;
\.


--
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Tomek
--

SELECT pg_catalog.setval('public.answer_id_seq', 16, true);


--
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Tomek
--

SELECT pg_catalog.setval('public.comment_id_seq', 8, true);


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Tomek
--

SELECT pg_catalog.setval('public.question_id_seq', 13, true);


--
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Tomek
--

SELECT pg_catalog.setval('public.tag_id_seq', 3, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Tomek
--

SELECT pg_catalog.setval('public.users_id_seq', 20, true);


--
-- Name: answer pk_answer_id; Type: CONSTRAINT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);


--
-- Name: comment pk_comment_id; Type: CONSTRAINT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);


--
-- Name: question pk_question_id; Type: CONSTRAINT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);


--
-- Name: question_tag pk_question_tag_id; Type: CONSTRAINT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);


--
-- Name: tag pk_tag_id; Type: CONSTRAINT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_login_uindex; Type: INDEX; Schema: public; Owner: Tomek
--

CREATE UNIQUE INDEX users_login_uindex ON public.users USING btree (login);


--
-- Name: answer answer_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT answer_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: comment comment_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: comment fk_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES public.answer(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: question_tag fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: answer fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: comment fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: question_tag fk_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES public.tag(id);


--
-- Name: question question_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: Tomek
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT question_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

