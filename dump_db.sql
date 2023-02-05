--
-- PostgreSQL database dump
--

-- Dumped from database version 14.2
-- Dumped by pg_dump version 14.2

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
-- Name: reservations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reservations (
    reservation_id integer NOT NULL,
    start_time time without time zone,
    end_time time without time zone,
    date date,
    user_id integer,
    room_id integer,
    resv_descr character varying,
    occupancy integer,
    repeat boolean,
    repeat_interval integer
);


ALTER TABLE public.reservations OWNER TO postgres;

--
-- Name: reservations_reservation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reservations_reservation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reservations_reservation_id_seq OWNER TO postgres;

--
-- Name: reservations_reservation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reservations_reservation_id_seq OWNED BY public.reservations.reservation_id;


--
-- Name: rooms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms (
    room_id integer NOT NULL,
    building_id integer,
    capacity integer,
    room_descr character varying
);


ALTER TABLE public.rooms OWNER TO postgres;

--
-- Name: rooms_room_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rooms_room_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rooms_room_id_seq OWNER TO postgres;

--
-- Name: rooms_room_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rooms_room_id_seq OWNED BY public.rooms.room_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    user_name character varying,
    password character varying,
    email character varying
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: reservations reservation_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservations ALTER COLUMN reservation_id SET DEFAULT nextval('public.reservations_reservation_id_seq'::regclass);


--
-- Name: rooms room_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms ALTER COLUMN room_id SET DEFAULT nextval('public.rooms_room_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: reservations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reservations (reservation_id, start_time, end_time, date, user_id, room_id, resv_descr, occupancy, repeat, repeat_interval) FROM stdin;
\.


--
-- Data for Name: rooms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rooms (room_id, building_id, capacity, room_descr) FROM stdin;
5	9	15	B9, Medium lab room with a table and chairs for 15 people
10	9	30	B9, Medium conference room with a table and chairs for 30 people
11	9	30	B9, Medium conference room with a table and chairs for 30 people
12	9	30	B9, Medium conference room with a table and chairs for 30 people
102	9	15	B9, Medium lab room with a table and chairs for 15 people
103	9	15	B9, Medium lab room with a table and chairs for 15 people
104	9	15	B9, Medium lab room with a table and chairs for 15 people
110	9	15	B9, Medium lab room with a table and chairs for 15 people
111	9	15	B9, Medium lab room with a table and chairs for 15 people
112	9	15	B9, Medium lab room with a table and chairs for 15 people
113	9	15	B9, Medium lab room with a table and chairs for 15 people
138	17	250	D17, Large conference room with a table and chairs for 250 people
241	17	154	D17, Large conference room with a table and chairs for 154 people
118	17	12	D17, Medium lab room with a table and chairs for 12 people
322	17	36	D17, Large lab room with a table and chairs for 36 people
323	17	36	D17, Large lab room with a table and chairs for 36 people
324	17	12	D17, Medium lab room with a table and chairs for 12 people
327	17	40	D17, Large lab room with a table and chairs for 40 people
3271	17	40	D17, Large lab room with a table and chairs for 40 people
3272	17	40	D17, Large lab room with a table and chairs for 40 people
3273	17	24	D17, Medium lab room with a table and chairs for 24 people
3274	17	20	D17, Medium lab room with a table and chairs for 20 people
201	6	176	D6, Large conference room with a table and chairs for 176 people
302	6	30	D6, Medium lab room with a table and chairs for 30 people
1	6	32	D6, Medium lab room with a table and chairs for 20 people
2	6	12	D6, Medium lab room with a table and chairs for 12 people
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, user_name, password, email) FROM stdin;
\.


--
-- Name: reservations_reservation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reservations_reservation_id_seq', 1, false);


--
-- Name: rooms_room_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_room_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);


--
-- Name: reservations reservations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_pkey PRIMARY KEY (reservation_id);


--
-- Name: rooms rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_pkey PRIMARY KEY (room_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: reservations reservations_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.rooms(room_id);


--
-- Name: reservations reservations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

